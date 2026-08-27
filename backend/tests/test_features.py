"""Resources, projects, interviews, resume, market, notifications tests."""


def test_resources_listing_and_filtering(client):
    resp = client.get("/api/v1/resources", params={"career_id": 1})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) > 20
    for r in items:
        assert r["url"].startswith("http") or r["url"] == ""
        assert r["resource_type"] in ("docs", "video", "course", "book",
                                      "github", "practice", "tutorial", "certification")

    free_only = client.get("/api/v1/resources", params={"is_free": True, "limit": 500}).json()
    assert all(r["is_free"] for r in free_only)


def test_resources_for_skill(client, career_id):
    roadmap = client.get(f"/api/v1/careers/{career_id}/roadmap").json()
    python_node = next(n for n in roadmap["nodes"] if n["skill"]["slug"] == "python")
    resp = client.get(f"/api/v1/resources/skill/{python_node['skill_id']}")
    assert resp.status_code == 200
    resources = resp.json()
    assert len(resources) >= 2
    assert any("python.org" in r["url"] or "freecodecamp" in r["url"] for r in resources)


def test_projects_flow(selected_auth_client, career_id):
    resp = selected_auth_client.get("/api/v1/projects", params={"career_id": career_id})
    assert resp.status_code == 200
    projects = resp.json()
    assert len(projects) >= 3
    difficulties = {p["difficulty"] for p in projects}
    assert difficulties <= {"beginner", "intermediate", "advanced"}
    for p in projects:
        assert p["milestones"], f"project {p['title']} missing milestones"
        assert p["rubric"]
        assert p["skills_demonstrated"], "projects must map to skills"

    project_id = projects[0]["id"]
    start = selected_auth_client.post(
        f"/api/v1/projects/{project_id}/progress",
        json={"status": "in_progress"})
    assert start.status_code == 200

    update = selected_auth_client.put(
        f"/api/v1/projects/{project_id}/progress",
        json={"completed_milestones": [0], "notes": "First milestone done"})
    assert update.status_code == 200
    body = update.json()
    assert 0 in body["completed_milestones"]

    complete = selected_auth_client.put(
        f"/api/v1/projects/{project_id}/progress",
        json={"status": "completed"})
    assert complete.status_code == 200
    assert complete.json()["progress"] == 100

    profile = selected_auth_client.get("/api/v1/profile").json()
    assert any(a["code"] == "first_project" and a["earned"] for a in profile["achievements"])


def test_interview_questions_flow(selected_auth_client):
    resp = selected_auth_client.get("/api/v1/interviews/questions")
    assert resp.status_code == 200
    questions = resp.json()
    assert len(questions) >= 10
    q = questions[0]

    upd = selected_auth_client.put(
        f"/api/v1/interviews/questions/{q['id']}",
        json={"mastered": True, "practiced": True, "confidence": 4})
    assert upd.status_code == 200
    assert upd.json()["mastered"] is True
    assert upd.json()["times_practiced"] == 1

    mastered_only = selected_auth_client.get(
        "/api/v1/interviews/questions", params={"mastered": True}).json()
    assert all(qq["mastered"] for qq in mastered_only)

    stats = selected_auth_client.get("/api/v1/interviews/stats").json()
    assert stats["total_questions"] >= 10
    assert stats["mastered_questions"] >= 1

    mock = selected_auth_client.post("/api/v1/interviews/mocks", json={
        "title": "Mock ML system design round", "category": "system_design"})
    assert mock.status_code == 200
    mid = mock.json()["id"]
    done = selected_auth_client.put(
        f"/api/v1/interviews/mocks/{mid}/complete", json={"score": 78, "notes": "went ok"})
    assert done.status_code == 200
    assert done.json()["score"] == 78


def test_resume_builder_flow(selected_auth_client, career_id):
    # complete some skills so the resume has verified material
    roadmap = selected_auth_client.get(f"/api/v1/careers/{career_id}/roadmap").json()
    # pick entry-level skills that also appear in the JD below
    jd_relevant = [n for n in roadmap["nodes"]
                   if n["skill"]["name"].lower().replace(" (cloud)", "").startswith("python")]
    core = [n for n in roadmap["nodes"]
            if "machine learning" in n["skill"]["name"].lower()][:1]
    chosen = (jd_relevant[:1] + core)[:2]
    assert chosen, "roadmap should contain python/ml skills"
    completed_ids = []
    for n in chosen:
        selected_auth_client.put(
            f"/api/v1/skills/{n['skill_id']}/progress", json={"status": "completed"})
        completed_ids.append(n["skill_id"])

    put = selected_auth_client.put("/api/v1/resume", json={
        "full_name": "Test User",
        "summary": "Aspiring AI/ML engineer with hands-on project experience.",
        "experience": [{"role": "Intern", "company": "Acme",
                        "start": "2025-01", "end": "2025-06",
                        "bullets": ["Built ETL pipeline"]}],
        "education": [{"degree": "B.Tech CSE", "institution": "Anna University",
                       "start": "2021", "end": "2025"}],
        "selected_skill_ids": completed_ids,
    })
    assert put.status_code == 200
    body = put.json()
    assert body["profile"]["full_name"] == "Test User"

    suggested = body["suggested_skills"]
    eligible = [s for s in suggested if s["eligible_for_resume"]]
    ineligible_completed = [
        s for s in suggested if s["id"] not in completed_ids and s["eligible_for_resume"]]
    # Only actually-completed skills may be resume-eligible
    assert set(s["id"] for s in eligible) <= set(completed_ids)
    assert ineligible_completed == []

    # analyze against a saved job
    job = selected_auth_client.post("/api/v1/jobs/analyze", json={
        "title": "ML Engineer",
        "raw_text": "Requirements: Python programming, machine learning, "
                    "Docker containerization, Kubernetes. Preferred: PyTorch.",
    }).json()
    link = selected_auth_client.put("/api/v1/resume", json={"target_job_id": job["id"]})
    analysis = link.json()["analysis"]
    assert analysis["jd_keywords"], "JD keywords should be extracted"
    assert analysis["keyword_coverage"] > 0
    assert "machine learning" in [k.lower() for k in analysis["matched_skills"]] or \
           analysis["matched_skills"]


def test_market_endpoint(client):
    resp = client.get("/api/v1/market/ai-ml-engineer")
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_demo_data"] is True  # clearly labelled demo data
    assert data["hiring_demand_index"] > 0
    cities = set(data["salary_ranges"]["entry"].keys())
    for expected in ("chennai", "bangalore", "hyderabad", "remote"):
        assert expected in cities
    assert len(data["most_requested_skills"]) >= 5
    assert len(data["top_companies"]) >= 5

    missing = client.get("/api/v1/market/nonexistent-career")
    assert missing.status_code == 404


def test_notifications_flow(selected_auth_client):
    unread = selected_auth_client.get("/api/v1/notifications", params={"unread_only": True}).json()
    assert isinstance(unread, list)

    count = selected_auth_client.get("/api/v1/notifications/unread-count").json()
    assert count["count"] >= 0

    marked = selected_auth_client.put("/api/v1/notifications/read-all")
    assert marked.status_code == 200
    after = selected_auth_client.get("/api/v1/notifications/unread-count").json()
    assert after["count"] == 0


def test_evidence_upload_metadata(selected_auth_client):
    roadmap = selected_auth_client.get("/api/v1/careers/1/roadmap").json()
    sid = roadmap["nodes"][0]["skill_id"]
    ev = selected_auth_client.post(f"/api/v1/skills/{sid}/evidence", json={
        "title": "Coursera certificate",
        "url": "https://coursera.org/verify/example",
        "evidence_type": "certificate",
        "description": "Completed with distinction",
    })
    assert ev.status_code == 200
    listing = selected_auth_client.get(f"/api/v1/skills/{sid}/evidence")
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    bad_url = selected_auth_client.post(f"/api/v1/skills/{sid}/evidence", json={
        "title": "bad", "url": "javascript:alert(1)"})
    assert bad_url.status_code == 400
