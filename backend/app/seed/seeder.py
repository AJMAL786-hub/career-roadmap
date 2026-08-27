"""Database seeding: careers, skills, DAG, resources, projects, questions,
achievements, roadmap versions. Idempotent — safe to run repeatedly."""
import json
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.career import CareerPath
from app.models.learning import LearningResource
from app.models.notification import Achievement, RoadmapVersion
from app.models.project import Project, ProjectSkill
from app.models.interview import InterviewQuestion

from app.seed.careers import aiml, datascience, fullstack, devops, cybersecurity
from app.seed.data_projects import PROJECTS
from app.seed.data_questions import QUESTIONS

logger = logging.getLogger(__name__)

CAREER_MODULES = [aiml, datascience, fullstack, devops, cybersecurity]

ACHIEVEMENTS = [
    {"code": "first_skill", "title": "First Steps", "description": "Completed your first skill", "icon": "sprout", "xp_reward": 25},
    {"code": "ten_skills", "title": "Double Digits", "description": "Completed 10 skills", "icon": "medal", "xp_reward": 100},
    {"code": "twenty_five_skills", "title": "Quarter Century", "description": "Completed 25 skills", "icon": "trophy", "xp_reward": 250},
    {"code": "first_session", "title": "Study Buddy", "description": "Logged your first study session", "icon": "book-open", "xp_reward": 25},
    {"code": "session_regular", "title": "Consistent Learner", "description": "Logged 25 study sessions", "icon": "calendar-check", "xp_reward": 150},
    {"code": "streak_7", "title": "Week Warrior", "description": "7-day study streak", "icon": "flame", "xp_reward": 100},
    {"code": "streak_30", "title": "Unstoppable", "description": "30-day study streak", "icon": "zap", "xp_reward": 500},
    {"code": "first_project", "title": "Shipper", "description": "Completed your first portfolio project", "icon": "rocket", "xp_reward": 100},
    {"code": "three_projects", "title": "Portfolio Builder", "description": "Completed 3 portfolio projects", "icon": "folder-git-2", "xp_reward": 200},
]


def slugify(value: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _seed_achievements(db: Session):
    for spec in ACHIEVEMENTS:
        existing = db.query(Achievement).filter(Achievement.code == spec["code"]).first()
        if not existing:
            db.add(Achievement(**spec))
    db.flush()


def seed_career(db: Session, module) -> None:
    meta = module.CAREER
    career = db.query(CareerPath).filter(CareerPath.slug == meta["slug"]).first()
    if not career:
        career = CareerPath(
            title=meta["title"], slug=meta["slug"], description=meta["description"],
            icon=meta["icon"], color=meta["color"], difficulty=meta.get("difficulty", "intermediate"),
            typical_roles=json.dumps(meta.get("typical_roles", [])),
            major_technologies=json.dumps(meta.get("major_technologies", [])),
        )
        db.add(career)
        db.flush()
    else:
        # update mutable metadata on re-seed
        career.description = meta["description"]
        career.difficulty = meta.get("difficulty", "intermediate")
        career.typical_roles = json.dumps(meta.get("typical_roles", []))
        career.major_technologies = json.dumps(meta.get("major_technologies", []))

    # ---- skills ----
    skill_by_key = {}
    existing_skills = {s.slug: s for s in _career_skills(db, career.id)}
    total_hours = 0

    from app.models.skill import Skill, SkillAlias, RoadmapNode, RoadmapEdge
    for spec in module.SKILLS:
        key = spec["key"]
        skill = existing_skills.get(key)
        if not skill:
            skill = Skill(
                career_path_id=career.id, name=spec["name"], slug=key,
                description=spec.get("description", ""), why_important=spec.get("why_important", ""),
                level=spec.get("level", "fundamental"), category=spec.get("category", "technical"),
                priority=spec.get("priority", "recommended"), estimated_hours=spec.get("hours", 10),
            )
            db.add(skill)
            db.flush()
            existing_skills[key] = skill
        else:
            skill.name = spec["name"]
            skill.description = spec.get("description", "")
            skill.level = spec.get("level", "fundamental")
            skill.category = spec.get("category", "technical")
            skill.priority = spec.get("priority", "recommended")
            skill.estimated_hours = spec.get("hours", 10)

        skill_by_key[key] = skill.id
        total_hours += spec.get("hours", 10)

        # aliases
        current_aliases = {a.alias.lower() for a in skill.aliases}
        for alias in spec.get("aliases", []) or []:
            if alias.lower() not in current_aliases:
                db.add(SkillAlias(skill_id=skill.id, alias=alias))
                current_aliases.add(alias.lower())

        # resources (idempotent by title)
        current_res = {r.title: r for r in db.query(LearningResource).filter(LearningResource.skill_id == skill.id).all()}
        for r in spec.get("resources", []) or []:
            res = current_res.get(r["title"])
            if not res:
                db.add(LearningResource(
                    skill_id=skill.id, title=r["title"], url=r.get("url", ""),
                    resource_type=r.get("type", "docs"), platform=r.get("platform", ""),
                    is_free=1 if r.get("free", True) else 0,
                    difficulty=r.get("difficulty", "beginner"),
                    estimated_hours=r.get("hours", 0),
                ))

    career.estimated_hours = total_hours

    # ---- DAG edges + node positions (layered layout) ----
    edges = [(a, b) for a, b in module.EDGES if a in skill_by_key and b in skill_by_key]

    # compute layers via longest-path from sources (DAG)
    prereq_map = {k: [] for k in skill_by_key}
    dependents_map = {k: [] for k in skill_by_key}
    for a, b in edges:
        prereq_map[b].append(a)
        dependents_map[a].append(b)

    layer_cache = {}

    def layer_of(key, visiting=None):
        visiting = visiting or set()
        if key in layer_cache:
            return layer_cache[key]
        if key in visiting:
            return 0
        visiting.add(key)
        parents = prereq_map[key]
        result = 0 if not parents else 1 + max(layer_of(p, visiting) for p in parents)
        visiting.discard(key)
        layer_cache[key] = result
        return result

    keys = list(skill_by_key.keys())
    layers = {k: layer_of(k) for k in keys}

    existing_nodes = {n.skill_id: n for n in _career_nodes(db, career.id)}
    from app.models.skill import RoadmapNode as RN, RoadmapEdge as RE
    for key in keys:
        sid = skill_by_key[key]
        layer = layers[key]
        if sid not in existing_nodes:
            db.add(RN(
                career_path_id=career.id, skill_id=sid, layer=layer,
                position_x=float(layer) * 260.0,
                position_y=float(_column_index(keys, key, layers)) * 110.0 + (layer % 2) * 40,
            ))
        else:
            existing_nodes[sid].layer = layer
            existing_nodes[sid].position_x = float(layer) * 260.0
            existing_nodes[sid].position_y = float(_column_index(keys, key, layers)) * 110.0 + (layer % 2) * 40

    existing_edges = {
        (e.source_skill_id, e.target_skill_id): e
        for e in db.query(RE).filter(RE.career_path_id == career.id).all()
    }
    for a, b in edges:
        pair = (skill_by_key[a], skill_by_key[b])
        if pair not in existing_edges:
            db.add(RE(career_path_id=career.id, source_skill_id=pair[0], target_skill_id=pair[1]))

    db.flush()

    # ---- projects ----
    for p in PROJECTS:
        if p["career"] != meta["slug"]:
            continue
        slug = slugify(p["title"])
        exists = db.query(Project).filter(Project.slug == slug, Project.career_path_id == career.id).first()
        if exists:
            continue
        project = Project(
            career_path_id=career.id, title=p["title"], slug=slug,
            description=p["description"], difficulty=p["difficulty"],
            estimated_hours=p["hours"],
            technologies=json.dumps(p["technologies"]),
            milestones=json.dumps(p["milestones"]),
            deliverables=json.dumps(p["deliverables"]),
            rubric=json.dumps(p["rubric"]),
        )
        db.add(project)
        db.flush()
        for sk in p.get("skills", []):
            sid = skill_by_key.get(sk)
            if sid:
                db.add(ProjectSkill(project_id=project.id, skill_id=sid))

    # ---- interview questions ----
    for q in QUESTIONS.get(meta["slug"], []):
        sid = skill_by_key.get(q.get("skill"))
        exists = db.query(InterviewQuestion).filter(
            InterviewQuestion.career_path_id == career.id,
            InterviewQuestion.question == q["q"],
        ).first()
        if not exists:
            db.add(InterviewQuestion(
                career_path_id=career.id, skill_id=sid,
                question=q["q"], answer=q.get("a", ""),
                difficulty=q.get("difficulty", "intermediate"),
                category=q.get("category", "programming"),
            ))

    # ---- roadmap version snapshot ----
    version = db.query(RoadmapVersion).filter(RoadmapVersion.career_path_id == career.id).first()
    if not version:
        db.add(RoadmapVersion(
            career_path_id=career.id, version="1.0.0", status="active",
            changelog="Initial seeded roadmap",
            skill_frequency_snapshot="{}",
        ))


def _career_skills(db: Session, career_id: int):
    from app.models.skill import Skill
    return db.query(Skill).filter(Skill.career_path_id == career_id).all()


def _career_nodes(db: Session, career_id: int):
    from app.models.skill import RoadmapNode
    return db.query(RoadmapNode).filter(RoadmapNode.career_path_id == career_id).all()


def _column_index(keys, target, layers):
    """Stable vertical ordering within a layer."""
    same_layer = sorted([k for k in keys if layers[k] == layers[target]])
    return same_layer.index(target)


def _seed_demo_user(db: Session) -> None:
    from app.models.user import User
    from app.models.skill import Skill, UserSkill, StudySession
    from app.models.notification import Notification
    from app.auth import get_password_hash
    from datetime import datetime, timezone, timedelta

    demo_email = "alex.chen@example.com"
    user = db.query(User).filter(User.email == demo_email).first()
    now = datetime.now(timezone.utc)
    if not user:
        user = User(
            email=demo_email,
            username="alexchen",
            hashed_password=get_password_hash("password123"),
            full_name="Alex Chen",
            selected_career_id=1,
            xp=650,
            onboarding_completed=True,
        )
        db.add(user)
        db.flush()

        ai_skills = db.query(Skill).filter(Skill.career_path_id == 1).order_by(Skill.id.asc()).all()
        for s in ai_skills[:6]:
            db.add(UserSkill(
                user_id=user.id,
                skill_id=s.id,
                status="completed",
                progress=100,
                started_at=now - timedelta(days=14),
                completed_at=now - timedelta(days=3),
            ))
        for s in ai_skills[6:9]:
            db.add(UserSkill(
                user_id=user.id,
                skill_id=s.id,
                status="in_progress",
                progress=60,
                started_at=now - timedelta(days=2),
            ))

        for i in range(7):
            db.add(StudySession(
                user_id=user.id,
                duration_minutes=45,
                notes=f"Deep work on AI/ML foundations & PyTorch tensors (Day {7-i})",
                session_date=now - timedelta(days=i),
            ))

        db.add(Notification(
            user_id=user.id,
            type="achievement",
            title="Welcome to CareerPath AI!",
            body="Your AI/ML career roadmap is active with 6 mastered skills & 7-day study streak.",
            link="/roadmap",
        ))
        db.flush()


def run_seed() -> dict:
    """Seed the full database. Returns summary counts."""
    from app.database import init_db
    init_db()
    started = datetime.now(timezone.utc)
    db = SessionLocal()
    try:
        _seed_achievements(db)
        counts = {}
        for module in CAREER_MODULES:
            seed_career(db, module)
            counts[module.CAREER["slug"]] = len(module.SKILLS)
        _seed_demo_user(db)
        db.commit()
        elapsed = (datetime.now(timezone.utc) - started).total_seconds()
        logger.info("Seeded %s in %.2fs", counts, elapsed)
        return {"careers": counts, "seconds": round(elapsed, 2)}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_seed())
