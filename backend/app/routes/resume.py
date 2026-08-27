from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import json
import io
from typing import List

from app.database import get_db
from app.models.resume import ResumeProfile, ATSScore
from app.models.career import CareerPath
from app.models.skill import Skill
from app.models.job import JobDescription
from app.auth import get_current_user
from app.models.user import User
from app.schemas.misc import ResumeProfileUpdate, ResumeAnalysis, ResumeResponse
from app.services.normalizer import canonical_key

router = APIRouter(prefix="/resume", tags=["Resume Builder"])

DEFAULTS = {
    "full_name": "", "email": "", "phone": "", "location": "",
    "linkedin_url": "", "github_url": "", "portfolio_url": "",
    "summary": "", "experience": [], "education": [], "certifications": [],
    "projects": [], "achievements": [], "selected_skill_ids": [],
}


def _get_or_create_profile(db: Session, user: User) -> ResumeProfile:
    profile = db.query(ResumeProfile).filter(ResumeProfile.user_id == user.id).first()
    if not profile:
        profile = ResumeProfile(
            user_id=user.id,
            full_name=user.full_name or user.username,
            email=user.email,
            target_career_id=user.selected_career_id,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def _profile_dict(profile: ResumeProfile) -> dict:
    return {
        "full_name": profile.full_name or "",
        "email": profile.email or "",
        "phone": profile.phone or "",
        "location": profile.location or "",
        "linkedin_url": profile.linkedin_url or "",
        "github_url": profile.github_url or "",
        "portfolio_url": profile.portfolio_url or "",
        "summary": profile.summary or "",
        "target_career_id": profile.target_career_id,
        "target_job_id": profile.target_job_id,
        "experience": json.loads(profile.experience or "[]"),
        "education": json.loads(profile.education or "[]"),
        "certifications": json.loads(profile.certifications or "[]"),
        "projects": json.loads(profile.projects or "[]"),
        "achievements": json.loads(profile.achievements or "[]"),
        "selected_skill_ids": json.loads(profile.selected_skill_ids or "[]"),
    }


@router.get("", response_model=ResumeResponse)
@router.get("/profile", response_model=ResumeResponse)
def get_resume(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_or_create_profile(db, user)
    analysis = _analyze_against_target(db, profile)
    suggested = _suggest_skills(db, user, profile)
    return ResumeResponse(
        profile=_profile_dict(profile),
        suggested_skills=suggested,
        analysis=analysis,
        updated_at=profile.updated_at,
    )


@router.put("", response_model=ResumeResponse)
@router.put("/profile", response_model=ResumeResponse)
def update_resume(
    data: ResumeProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    def _url_ok(u):
        return u is None or u == "" or u.startswith(("http://", "https://"))

    for field in ("linkedin_url", "github_url", "portfolio_url"):
        val = getattr(data, field)
        if val is not None and not _url_ok(val):
            raise HTTPException(status_code=400, detail=f"{field} must be a valid http(s) URL")

    profile = _get_or_create_profile(db, user)
    simple = ["full_name", "email", "phone", "location", "linkedin_url",
              "github_url", "portfolio_url", "summary"]
    for f in simple:
        v = getattr(data, f)
        if v is not None:
            setattr(profile, f, str(v)[:3000])
    if data.target_career_id is not None:
        career = db.query(CareerPath).filter(CareerPath.id == data.target_career_id).first()
        if not career:
            raise HTTPException(status_code=404, detail="Career not found")
        profile.target_career_id = career.id
    if data.target_job_id is not None:
        job = db.query(JobDescription).filter(
            JobDescription.user_id == user.id, JobDescription.id == data.target_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        profile.target_job_id = job.id

    list_fields = {
        "experience": "experience", "education": "education",
        "certifications": "certifications", "projects": "projects",
    }
    for attr, col in list_fields.items():
        v = getattr(data, attr)
        if v is not None:
            setattr(profile, col, json.dumps([i.model_dump() for i in v])[:50000])
    if data.achievements is not None:
        profile.achievements = json.dumps([str(a)[:300] for a in data.achievements[:20]])
    if data.selected_skill_ids is not None:
        valid = [sid for sid in data.selected_skill_ids[:40]
                 if isinstance(sid, int) and db.query(Skill).filter(Skill.id == sid).first()]
        profile.selected_skill_ids = json.dumps(valid)

    db.commit()
    analysis = _analyze_against_target(db, profile)
    suggested = _suggest_skills(db, user, profile)
    return ResumeResponse(
        profile=_profile_dict(profile), suggested_skills=suggested,
        analysis=analysis, updated_at=profile.updated_at,
    )


@router.post("/analyze")
def analyze_resume_text(
    payload: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ATS keyword scanning against career requirements."""
    resume_text = payload.get("resume_text", "")
    career_id = payload.get("career_id") or user.selected_career_id
    
    # Get relevant career skills
    skills_query = db.query(Skill)
    if career_id:
        skills_query = skills_query.filter(Skill.career_path_id == career_id)
    skills = skills_query.all()
    
    text_lower = resume_text.lower()
    matched_keywords = []
    missing_keywords = []
    
    for s in skills:
        # Check skill name and aliases
        name_match = s.name.lower() in text_lower
        alias_match = any(a.alias.lower() in text_lower for a in s.aliases)
        if name_match or alias_match:
            if s.name not in matched_keywords:
                matched_keywords.append(s.name)
        else:
            if s.priority == "must_have" and s.name not in missing_keywords:
                missing_keywords.append(s.name)
            elif len(missing_keywords) < 8 and s.name not in missing_keywords:
                missing_keywords.append(s.name)

    total_target = max(len(matched_keywords) + len(missing_keywords), 1)
    score = min(95, max(35, round((len(matched_keywords) / total_target) * 100))) if (matched_keywords or missing_keywords) else 65

    recs = [
        "Include metrics and business impact for each key technical achievement (e.g. 'Improved throughput by 35%').",
        "Add explicit architectural and infrastructure keywords in your experience section.",
        "Ensure all production tools, frameworks, and deployment environments match the job spec.",
    ]
    if missing_keywords:
        recs.insert(0, f"Consider highlighting hands-on project experience with {', '.join(missing_keywords[:3])}.")

    result = {
        "score": score,
        "matched_keywords": matched_keywords[:15],
        "missing_keywords": missing_keywords[:8],
        "recommendations": recs[:4],
    }
    _record_score(db, user, score, career_id or user.selected_career_id,
                  "scan", matched_keywords, missing_keywords)
    return result


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md", ".rtf", ".html", ".htm"}


def _extract_text(filename: str, data: bytes) -> str:
    """Extract plain text from a resume file (PDF / DOCX / plain text)."""
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            raise HTTPException(status_code=400, detail="Could not read PDF. Please upload a text-based PDF.")
    if name.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(data))
            parts = [p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            parts.append(cell.text)
            return "\n".join(parts)
        except Exception:
            raise HTTPException(status_code=400, detail="Could not read DOCX. Please ensure the file is a valid .docx.")
    # Plain text / markdown / RTF-ish fallback
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a resume file (PDF/DOCX/TXT) and score it against the target role."""
    filename = file.filename or "resume"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, DOCX, or TXT resume.",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB).")

    resume_text = _extract_text(filename, data)
    if len(resume_text.strip()) < 40:
        raise HTTPException(
            status_code=400,
            detail="Not enough readable text found in the resume. Try a text-based (non-scanned) PDF.",
        )

    # Optionally persist the extracted resume for reuse in the ATS scanner.
    _get_or_create_profile(db, user)
    profile = db.query(ResumeProfile).filter(ResumeProfile.user_id == user.id).first()
    if profile and not profile.summary:
        profile.summary = resume_text[:3000]
        db.commit()

    career_id = user.selected_career_id
    skills_query = db.query(Skill)
    if career_id:
        skills_query = skills_query.filter(Skill.career_path_id == career_id)
    skills = skills_query.all()

    text_lower = resume_text.lower()
    matched_keywords = []
    missing_keywords = []
    for s in skills:
        name_match = s.name.lower() in text_lower
        alias_match = any(a.alias.lower() in text_lower for a in s.aliases)
        if name_match or alias_match:
            if s.name not in matched_keywords:
                matched_keywords.append(s.name)
        else:
            if s.priority == "must_have" and s.name not in missing_keywords:
                missing_keywords.append(s.name)
            elif len(missing_keywords) < 8 and s.name not in missing_keywords:
                missing_keywords.append(s.name)

    total_target = max(len(matched_keywords) + len(missing_keywords), 1)
    score = min(95, max(35, round((len(matched_keywords) / total_target) * 100))) if (matched_keywords or missing_keywords) else 65

    recs = [
        "Quantify every technical achievement with metrics and business impact (e.g. 'Cut inference latency by 42%').",
        "Mirror the job spec's exact tool names, frameworks, and deployment keywords in your experience bullets.",
        "Use standard section headers (Experience, Skills, Education) so ATS parsers can index your resume cleanly.",
    ]
    if missing_keywords:
        recs.insert(0, f"Add hands-on evidence for: {', '.join(missing_keywords[:3])}.")

    _record_score(db, user, score, career_id or user.selected_career_id,
                  "upload", matched_keywords, missing_keywords)

    return {
        "score": score,
        "matched_keywords": matched_keywords[:15],
        "missing_keywords": missing_keywords[:8],
        "recommendations": recs[:4],
        "filename": filename,
        "extracted_text": resume_text,
    }


def _record_score(db: Session, user: User, score: int, career_id, source: str,
                  matched_keywords: List[str], missing_keywords: List[str]) -> None:
    """Persist an ATS score snapshot so users can track progress over time."""
    entry = ATSScore(
        user_id=user.id,
        score=score,
        career_id=career_id,
        source=source,
        matched_keywords=json.dumps(matched_keywords[:15]),
        missing_keywords=json.dumps(missing_keywords[:8]),
    )
    db.add(entry)
    db.commit()


@router.get("/history")
def get_score_history(
    limit: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return recent ATS scores for trend/progress tracking."""
    limit = max(1, min(limit, 100))
    rows = (
        db.query(ATSScore)
        .filter(ATSScore.user_id == user.id)
        .order_by(ATSScore.created_at.desc(), ATSScore.id.desc())
        .limit(limit)
        .all()
    )
    history = [
        {
            "id": s.id,
            "score": s.score,
            "source": s.source,
            "career_id": s.career_id,
            "matched_keywords": json.loads(s.matched_keywords or "[]"),
            "missing_keywords": json.loads(s.missing_keywords or "[]"),
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }
        for s in rows
    ]
    history.reverse()
    latest = history[-1]["score"] if history else None
    first = history[0]["score"] if history else None
    delta = (latest - first) if (latest is not None and first is not None) else 0
    return {
        "history": history,
        "count": len(history),
        "latest_score": latest,
        "first_score": first,
        "trend": "up" if delta > 0 else ("down" if delta < 0 else "flat"),
        "delta": delta,
    }


def _suggest_skills(db: Session, user: User, profile: ResumeProfile) -> List[dict]:
    """Only recommend skills the user actually completed — never fabricate."""
    rows = db.query(Skill, ).filter(
        Skill.career_path_id == (profile.target_career_id or user.selected_career_id or -1),
    ).all() if (profile.target_career_id or user.selected_career_id) else []
    from app.models.skill import UserSkill
    states = {us.skill_id: us.status for us in db.query(UserSkill).filter(UserSkill.user_id == user.id).all()}
    result = []
    for s in rows:
        status = states.get(s.id, "not_started")
        result.append({
            "id": s.id, "name": s.name, "category": s.category,
            "priority": s.priority, "status": status,
            "eligible_for_resume": status == "completed" and s.category != "soft_skill",
        })
    return sorted(result, key=lambda x: (
        0 if x["eligible_for_resume"] else 1,
        {"must_have": 0, "recommended": 1, "optional": 2}.get(x["priority"], 1),
        x["name"],
    ))[:60]


def _analyze_against_target(db: Session, profile: ResumeProfile) -> ResumeAnalysis:
    """Compare the resume against the targeted JD keywords when available."""
    if not profile.target_job_id:
        return ResumeAnalysis()
    job = db.query(JobDescription).filter(JobDescription.id == profile.target_job_id).first()
    if not job:
        return ResumeAnalysis()

    jd_keywords = [canonical_key(js.normalized_name) for js in job.job_skills if js.normalized_name]
    jd_keywords = [k for k in jd_keywords if k]

    # Skills claimed on the resume come ONLY from verified user skill state
    selected_ids = set(json.loads(profile.selected_skill_ids or "[]"))
    from app.models.skill import UserSkill
    completed_rows = db.query(UserSkill).filter(
        UserSkill.user_id == profile.user_id, UserSkill.status == "completed").all()
    id_to_skill = {}
    if completed_rows:
        skills = db.query(Skill).filter(Skill.id.in_([r.skill_id for r in completed_rows])).all()
        id_to_skill = {s.id: s.name for s in skills}
    claimed_canonical = {canonical_key(id_to_skill[r.skill_id]) for r in completed_rows if r.skill_id in id_to_skill}

    matched = [k for k in jd_keywords if k in claimed_canonical]
    missing = [k for k in jd_keywords if k not in matched and k not in selected_ids]
    coverage = round(len(matched) / len(jd_keywords) * 100, 1) if jd_keywords else 0.0
    return ResumeAnalysis(
        jd_keywords=sorted(set(jd_keywords))[:40],
        matched_skills=sorted(set(matched)),
        missing_keywords=sorted(set(missing))[:25],
        keyword_coverage=coverage,
    )
