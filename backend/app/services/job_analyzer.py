import re
from typing import List, Tuple, Dict
from sqlalchemy.orm import Session
from app.models.skill import Skill, SkillAlias, UserSkill
from app.models.job import JobDescription, JobSkill
from app.models.user import User
from app.schemas.job import JobAnalyzeRequest, JobAnalysisResponse, ExtractedSkill

# Common skill aliases for normalization
ALIAS_MAP = {
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "python 3": "python",
    "python programming": "python",
    "py": "python",
    "js": "javascript",
    "javascript": "javascript",
    "typescript": "typescript",
    "ts": "typescript",
    "react.js": "react",
    "reactjs": "react",
    "react": "react",
    "node.js": "node.js",
    "nodejs": "node.js",
    "node": "node.js",
    "restful apis": "rest apis",
    "rest api development": "rest apis",
    "rest api": "rest apis",
    "rest apis": "rest apis",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "deep learning": "deep learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",
    "ci/cd": "ci/cd",
    "cicd": "ci/cd",
    "ci cd": "ci/cd",
    "aws": "aws",
    "amazon web services": "aws",
    "gcp": "google cloud",
    "google cloud platform": "google cloud",
    "azure": "azure",
    "microsoft azure": "azure",
    "docker": "docker",
    "containerization": "docker",
    "sql": "sql",
    "structured query language": "sql",
    "nosql": "nosql",
    "mongodb": "mongodb",
    "mongo": "mongodb",
    "postgresql": "postgresql",
    "postgres": "postgresql",
    "mysql": "mysql",
    "linux": "linux",
    "git": "git",
    "github": "git",
    "terraform": "terraform",
    "ansible": "ansible",
    "jenkins": "jenkins",
    "tensorflow": "tensorflow",
    "tf": "tensorflow",
    "pytorch": "pytorch",
    "torch": "pytorch",
    "pandas": "pandas",
    "numpy": "numpy",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "html": "html",
    "css": "css",
    "html5": "html",
    "css3": "css",
    "graphql": "graphql",
    "redis": "redis",
    "kafka": "kafka",
    "rabbitmq": "rabbitmq",
    "agile": "agile",
    "scrum": "scrum",
}


def normalize_skill_name(name: str) -> str:
    key = name.lower().strip()
    return ALIAS_MAP.get(key, key)


def extract_skills_from_text(text: str) -> List[Tuple[str, str]]:
    """Extract skill mentions from job description text. Returns list of (original, normalized)."""
    text_lower = text.lower()
    found = []
    seen_normalized = set()

    # Check all known aliases
    for alias, normalized in sorted(ALIAS_MAP.items(), key=lambda x: -len(x[0])):
        pattern = r'\b' + re.escape(alias) + r'\b'
        if re.search(pattern, text_lower):
            if normalized not in seen_normalized:
                found.append((alias, normalized))
                seen_normalized.add(normalized)

    return found


def analyze_job(db: Session, user: User, request: JobAnalyzeRequest) -> JobAnalysisResponse:
    # Extract skills from text
    extracted = extract_skills_from_text(request.raw_text)

    # Save job description
    job = JobDescription(
        user_id=user.id,
        title=request.title or "Untitled Position",
        company=request.company or "Unknown",
        raw_text=request.raw_text,
    )
    db.add(job)
    db.flush()

    # Get user's career path skills
    career_skills = []
    if user.selected_career_id:
        career_skills = db.query(Skill).filter(Skill.career_path_id == user.selected_career_id).all()

    # Build lookup: normalized_name -> Skill
    skill_lookup: Dict[str, Skill] = {}
    for s in career_skills:
        skill_lookup[s.name.lower()] = s
        for alias_obj in s.aliases:
            skill_lookup[alias_obj.alias.lower()] = s

    # Get user skill statuses
    user_skill_map = {}
    if career_skills:
        user_skills = db.query(UserSkill).filter(
            UserSkill.user_id == user.id,
            UserSkill.skill_id.in_([s.id for s in career_skills])
        ).all()
        user_skill_map = {us.skill_id: us for us in user_skills}

    exact_matches = []
    partial_matches = []
    missing_skills = []

    for original, normalized in extracted:
        matched_skill = skill_lookup.get(normalized)
        if not matched_skill:
            # Try partial match
            for sname, s in skill_lookup.items():
                if normalized in sname or sname in normalized:
                    matched_skill = s
                    break

        es = ExtractedSkill(
            skill_name=original,
            normalized_name=normalized,
            requirement_type="required",
        )

        if matched_skill:
            es.matched_skill_id = matched_skill.id
            es.is_matched = True
            us = user_skill_map.get(matched_skill.id)
            if us:
                es.user_status = us.status
                if us.status == "completed":
                    exact_matches.append(es)
                else:
                    partial_matches.append(es)
            else:
                partial_matches.append(es)
        else:
            missing_skills.append(es)

        # Save job skill record
        js = JobSkill(
            job_description_id=job.id,
            skill_name=original,
            normalized_name=normalized,
            matched_skill_id=matched_skill.id if matched_skill else None,
            is_matched=1 if matched_skill else 0,
        )
        db.add(js)

    total_required = len(extracted)
    total_matched = len(exact_matches) + len(partial_matches)
    match_score = round((len(exact_matches) / total_required) * 100, 1) if total_required > 0 else 0

    job.match_score = match_score
    db.commit()

    # Find overqualified (skills user has but job doesn't require)
    overqualified = []
    required_skill_ids = {es.matched_skill_id for es in exact_matches + partial_matches + missing_skills if es.matched_skill_id}
    for skill in career_skills:
        us = user_skill_map.get(skill.id)
        if us and us.status == "completed" and skill.id not in required_skill_ids:
            overqualified.append(ExtractedSkill(
                skill_name=skill.name,
                normalized_name=skill.name.lower(),
                is_matched=True,
                matched_skill_id=skill.id,
                user_status="completed",
            ))

    return JobAnalysisResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        match_score=match_score,
        exact_matches=exact_matches,
        partial_matches=partial_matches,
        missing_skills=missing_skills,
        overqualified=overqualified[:5],
        total_required=total_required,
        total_matched=total_matched,
    )
