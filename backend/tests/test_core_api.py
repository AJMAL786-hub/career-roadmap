"""Core API tests: careers, roadmap, skills, progress, dashboard."""


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_list_careers(client):
    resp = client.get("/api/v1/careers")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 5
    slugs = {c["slug"] for c in data}
    assert "ai-ml-engineer" in slugs
    for c in data:
        assert c["skill_count"] > 0
        assert c["estimated_hours"] > 0
        assert isinstance(c["typical_roles"], list)


def test_get_career_detail(client):
    resp = client.get("/api/v1/careers/1")
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "AI/ML Engineer"
    assert len(body["major_technologies"]) > 3


def test_get_career_404(client):
    resp = client.get("/api/v1/careers/999")
    assert resp.status_code == 404


def test_roadmap_retrieval_with_dag(client, career_id):
    resp = client.get(f"/api/v1/careers/{career_id}/roadmap")
    assert resp.status_code == 200
    body = resp.json()
    nodes = body["nodes"]
    edges = body["edges"]
    assert len(nodes) >= 25
    assert len(edges) > len(nodes) // 2

    # verify DAG: no cycles via Kahn's algorithm
    from collections import defaultdict, deque
    adj = defaultdict(list)
    indeg = defaultdict(int)
    skill_ids = set()
    for n in nodes:
        skill_ids.add(n["skill_id"])
    for e in edges:
        if e["source_skill_id"] in skill_ids and e["target_skill_id"] in skill_ids:
            adj[e["source_skill_id"]].append(e["target_skill_id"])
            indeg[e["target_skill_id"]] += 1
    queue = deque([sid for sid in skill_ids if indeg[sid] == 0])
    seen = 0
    while queue:
        cur = queue.popleft()
        seen += 1
        for nxt in adj[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    assert seen == len(skill_ids), "Roadmap graph contains a cycle!"

    # layered positions exist
    layers = [n["layer"] for n in nodes]
    assert min(layers) == 0
    assert max(layers) >= 2


def test_auth_flow_and_validation(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "weakpass@example.com",
        "username": "weakpass",
        "password": "short",
    })
    assert resp.status_code == 422  # password policy enforced

    import random
    suffix = random.randint(100000, 999999)
    resp = client.post("/api/v1/auth/register", json={
        "email": f"flow{suffix}@example.com",
        "username": f"flow{suffix}",
        "password": "Passw0rd123",
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200

    bad = client.post("/api/v1/auth/login", json={
        "email": f"flow{suffix}@example.com", "password": "WrongPass1"})
    assert bad.status_code == 401


def test_unauthenticated_dashboard_blocked(client):
    resp = client.get("/api/v1/dashboard")
    assert resp.status_code == 401


def test_skill_progress_update_and_completion(selected_auth_client):
    # pick a fundamental node (no prerequisites) — python is layer 0
    roadmap = selected_auth_client.get("/api/v1/careers/1/roadmap").json()
    python_node = next(n for n in roadmap["nodes"] if n["skill"]["slug"] == "python")
    sid = python_node["skill_id"]

    resp = selected_auth_client.put(f"/api/v1/skills/{sid}/progress", json={
        "status": "in_progress", "progress": 40})
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"

    resp = selected_auth_client.put(f"/api/v1/skills/{sid}/progress", json={
        "status": "completed", "confidence": 4,
        "notes": "Finished the official tutorial"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "completed"
    assert body["progress"] == 100
    assert body["completed_at"] is not None

    # invalid status rejected
    bad = selected_auth_client.put(f"/api/v1/skills/{sid}/progress", json={
        "status": "done_already"})
    assert bad.status_code == 422


def test_custom_skill_creation_appears_in_calculations(selected_auth_client):
    resp = selected_auth_client.post("/api/v1/skills/custom", json={
        "career_path_id": 1,
        "name": "Prompt Chaining Patterns",
        "description": "Advanced multi-step prompt orchestration",
        "category": "technical",
        "priority": "recommended",
        "estimated_hours": 12,
        "level": "advanced",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_custom"] == 1
    custom_id = body["id"]

    roadmap = selected_auth_client.get("/api/v1/careers/1/roadmap").json()
    ids = [n["skill_id"] for n in roadmap["nodes"]]
    assert custom_id in ids

    # mark completed -> reflected in dashboard totals
    selected_auth_client.put(f"/api/v1/skills/{custom_id}/progress", json={"status": "completed"})
    dash = selected_auth_client.get("/api/v1/dashboard").json()
    skills_before = dash["completed_skills"]
    assert skills_before >= 1


def test_completion_calculation_on_dashboard(selected_auth_client):
    roadmap = selected_auth_client.get("/api/v1/careers/1/roadmap").json()
    total = len(roadmap["nodes"])
    first_two = roadmap["nodes"][:2]

    for n in first_two:
        r = selected_auth_client.put(
            f"/api/v1/skills/{n['skill_id']}/progress", json={"status": "completed"})
        assert r.status_code == 200

    dash = selected_auth_client.get("/api/v1/dashboard").json()
    assert dash["total_skills"] == total
    assert dash["completed_skills"] >= 2
    expected_min = round(2 / total * 100, 1)
    assert dash["overall_progress"] >= expected_min - 0.5
    assert dash["job_readiness_score"] > 0
    assert len(dash["recommended_next"]) >= 1
    assert dash["estimated_remaining_hours"] < sum(n["skill"]["estimated_hours"] for n in roadmap["nodes"])


def test_study_sessions_streak_and_xp(selected_auth_client):
    resp = selected_auth_client.post("/api/v1/study-sessions", json={
        "duration_minutes": 45, "notes": "Deep work block"})
    assert resp.status_code == 200

    stats = selected_auth_client.get("/api/v1/study-sessions/stats").json()
    assert stats["total_minutes"] >= 45
    assert "current_streak" in stats
    assert len(stats["weekly"]) == 7

    profile = selected_auth_client.get("/api/v1/profile").json()
    assert profile["gamification"]["xp"] > 0
    earned = [a for a in profile["achievements"] if a["earned"]]
    assert any(a["code"] in ("first_session",) for a in earned)
