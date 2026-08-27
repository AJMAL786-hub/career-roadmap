"""JD parsing, skill normalization, gap analysis tests."""
from app.services.normalizer import normalize_skill_name, best_fuzzy_match
from app.services.job_parser import JobParser


def test_normalization_aliases():
    assert normalize_skill_name("K8s") == "kubernetes"
    assert normalize_skill_name("Kubernetes orchestration") == "kubernetes"
    assert normalize_skill_name("Python 3") == "python"
    assert normalize_skill_name("Python programming") == "python"
    assert normalize_skill_name("RESTful API development") == "rest apis"
    assert normalize_skill_name("Postgres") == "postgresql"
    assert normalize_skill_name("sklearn") == "scikit-learn"
    assert normalize_skill_name("CI/CD pipelines") not in ("", None)
    assert normalize_skill_name("Amazon Web Services") == "aws"


def test_fuzzy_fallback():
    match = best_fuzzy_match("deep learning frameworks", ["deep learning", "docker"], threshold=0.6)
    assert match is not None and match[0] == "deep learning"


def test_jd_parser_extracts_and_classifies():
    jd = """Senior ML Engineer - Acme Corp

Requirements:
- 5+ years of experience in Python programming and machine learning
- Strong hands-on with PyTorch, K8s, Docker and AWS cloud
- Experience with RESTful API development and PostgreSQL databases
- Solid SQL skills

Preferred qualifications:
- Familiarity with LLMs, RAG pipelines and Kubernetes orchestration
- Nice to have: Terraform, CI/CD with GitHub Actions
"""
    parser = JobParser(["Python", "Machine Learning", "PyTorch", "Kubernetes",
                        "Docker", "AWS", "REST APIs", "PostgreSQL", "SQL",
                        "LLMs & RAG", "Terraform", "CI/CD Pipelines"])
    parsed = parser.parse(jd)

    canonicals = {s.canonical for s in parsed.skills}
    for expected in ("python", "machine learning", "pytorch", "kubernetes",
                     "docker", "aws", "rest apis", "postgresql"):
        assert expected in canonicals, f"missing {expected}: got {canonicals}"

    # required vs preferred split respected
    by_canon = {s.canonical: s for s in parsed.skills}
    assert by_canon["python"].requirement_type == "required"
    assert by_canon["llms & rag"].requirement_type == "preferred"

    # structured metadata extraction
    assert parsed.years_experience == 5
    assert any("Bachelor" in e or "Master" in e or "PhD" in e for e in parsed.education) or parsed.education == []
    assert len(parsed.soft_skills) >= 0  # soft skills optional in this JD


def test_gap_analysis_prioritizes_missing():
    from app.services.job_parser import ParsedJob, ExtractedSkill
    from app.services.gap_analyzer import GapAnalyzer

    parsed = ParsedJob(skills=[
        ExtractedSkill(raw="Python", canonical="python", requirement_type="required"),
        ExtractedSkill(raw="K8s", canonical="kubernetes", requirement_type="required"),
        ExtractedSkill(raw="Terraform", canonical="terraform", requirement_type="preferred"),
        ExtractedSkill(raw="Docker", canonical="docker", requirement_type="required"),
        ExtractedSkill(raw="GraphQL", canonical="graphql", requirement_type="required"),
    ])
    user_map = {
        "python": {"status": "completed", "confidence": 4, "skill_id": 1, "name": "Python"},
        "docker": {"status": "in_progress", "confidence": 2, "skill_id": 2, "name": "Docker"},
        "git": {"status": "completed", "confidence": 3, "skill_id": 9, "name": "Git"},
    }
    career_map = {
        "python": {"skill_id": 1, "priority": "must_have", "hours": 60},
        "kubernetes": {"skill_id": 3, "priority": "must_have", "hours": 35},
        "terraform": {"skill_id": 4, "priority": "recommended", "hours": 30},
        "docker": {"skill_id": 2, "priority": "must_have", "hours": 20},
        "graphql": {"skill_id": 5, "priority": "optional", "hours": 18},
    }

    report = GapAnalyzer().analyze(parsed, user_map, career_map)

    exact_names = {g.canonical for g in report.exact_matches}
    partial_names = {g.canonical for g in report.partial_matches}
    missing_names = {g.canonical for g in report.missing_required}
    pref_names = {g.canonical for g in report.missing_preferred}

    assert exact_names == {"python"}
    assert partial_names == {"docker"}
    assert missing_names == {"kubernetes"}
    assert pref_names == {"terraform"}

    # overqualified: git completed but not requested
    over_names = {g.canonical for g in report.overqualified}
    assert "git" in over_names

    # learn-first ranking puts required missing first
    assert report.learn_first[0].canonical == "kubernetes"
    labels = {g.priority_label for g in report.learn_first}
    assert "Critical" in labels or "High" in labels

    # score = completed required / total required (python only) = 1/3
    assert abs(report.match_score - 33.3) < 0.5


def test_full_pipeline_via_api(selected_auth_client):
    """End-to-end JD analysis through the API with a real seeded career."""
    jd_text = """
Senior DevOps Engineer - CloudScale Systems (Chennai)

We are looking for a DevOps engineer to join our platform team.

Requirements:
- 4+ years managing production workloads on AWS
- Expert-level Kubernetes and Docker containerization experience
- Strong Infrastructure as Code skills with Terraform
- Solid Linux administration and networking fundamentals
- CI/CD pipeline experience (GitHub Actions or Jenkins)

Preferred:
- Monitoring & observability with Prometheus and Grafana
- GitOps workflows (Argo CD)
- Python scripting ability
- Communication skills and on-call experience
"""
    resp = selected_auth_client.post("/api/v1/jobs/analyze", json={
        "title": "Senior DevOps Engineer",
        "company": "CloudScale Systems",
        "raw_text": jd_text,
    })
    assert resp.status_code == 200
    body = resp.json()

    canon = {g["canonical"] for g in body["exact_matches"] + body["partial_matches"]
             + body["missing_required"] + body["missing_preferred"]}
    for expected in ("linux", "kubernetes", "docker", "aws", "ci-cd", "terraform"):
        assert expected in canon, f"{expected} not extracted: {canon}"

    assert body["parsed_meta"]["years_experience"] == 4
    assert len(body["learn_first"]) >= 1
    # learn-first must be sorted by priority score desc
    scores = [g["priority_score"] for g in body["learn_first"]]
    assert scores == sorted(scores, reverse=True)

    job_id = body["id"]

    # saved job appears in listing + detail retrieval works
    jobs = selected_auth_client.get("/api/v1/jobs").json()
    assert any(j["id"] == job_id for j in jobs)

    detail = selected_auth_client.get(f"/api/v1/jobs/{job_id}")
    assert detail.status_code == 200

    # compare two saved analyses
    resp2 = selected_auth_client.post("/api/v1/jobs/analyze", json={
        "title": "ML Platform Engineer",
        "company": "OtherCorp",
        "raw_text": "Must have: Kubernetes orchestration, Postgres database, "
                    "Python 3 programming. Preferred: K8s security, Grafana dashboards.",
    })
    assert resp2.status_code == 200
    second_id = resp2.json()["id"]

    compare = selected_auth_client.post("/api/v1/jobs/compare", json=[job_id, second_id])
    assert compare.status_code == 200
    cbody = compare.json()
    assert len(cbody["jobs"]) == 2
    assert isinstance(cbody["common_missing"], list)
