"""RecommendationEngine service.

Recommends the next skills to learn based on DAG topology (unlocked nodes),
user progress, and career priorities. Designed so a smarter ML ranker can
replace the heuristic later without changing the interface.
"""
from typing import Dict, List, Optional


class RecommendationEngine:
    def __init__(self, nodes: List[dict], edges: List[dict], user_status: Dict[int, dict]):
        """nodes: [{skill_id, name, priority, level, hours, category}]
        edges: [{source_skill_id, target_skill_id}]
        user_status: skill_id -> {status: str, confidence: int}
        """
        self.nodes = {n["skill_id"]: n for n in nodes}
        self.prereqs: Dict[int, List[int]] = {n: [] for n in self.nodes}
        for e in edges:
            if e["target_skill_id"] in self.prereqs and e["source_skill_id"] in self.nodes:
                self.prereqs[e["target_skill_id"]].append(e["source_skill_id"])
        self.user_status = user_status

    def _state(self, skill_id: int) -> str:
        return self.user_status.get(skill_id, {}).get("status", "not_started")

    def is_unlocked(self, skill_id: int) -> bool:
        """A node is unlocked when all its prerequisites are completed."""
        return all(self._state(p) == "completed" for p in self.prereqs[skill_id])

    def classify_states(self) -> Dict[str, List[dict]]:
        """Return completed / in_progress / unlocked(recommended-next candidates)
        / locked node lists."""
        buckets: Dict[str, List[dict]] = {
            "completed": [], "in_progress": [], "recommended": [], "locked": [],
        }
        for sid, node in self.nodes.items():
            state = self._state(sid)
            entry = dict(node)
            entry["prerequisites"] = self.prereqs[sid]
            if state == "completed":
                buckets["completed"].append(entry)
            elif state == "in_progress":
                buckets["in_progress"].append(entry)
            elif self.is_unlocked(sid):
                buckets["recommended"].append(entry)
            else:
                entry["blocking_prereqs"] = [
                    p for p in self.prereqs[sid] if self._state(p) != "completed"
                ]
                buckets["locked"].append(entry)
        return buckets

    def recommend_next(self, limit: int = 3) -> List[dict]:
        """Rank recommended-next candidates: in-progress first, then unlocked
        must-haves by fewest prerequisites then fewest hours."""
        buckets = self.classify_states()
        in_prog = sorted(buckets["in_progress"], key=lambda n: n.get("hours", 10))
        recs = buckets["recommended"]

        def rank(n):
            priority_rank = {"must_have": 0, "recommended": 1, "optional": 2}.get(
                n.get("priority", "recommended"), 1)
            level_rank = {"fundamental": 0, "intermediate": 1, "advanced": 2,
                          "optional": 3}.get(n.get("level", "intermediate"), 1)
            return (priority_rank, len(n.get("prerequisites", [])), level_rank,
                    n.get("hours", 10))

        ranked = sorted(recs, key=rank)
        result = []
        for n in in_prog[:limit]:
            result.append({**n, "reason": "You're already working on this"})
        for n in ranked:
            if len(result) >= limit:
                break
            result.append({
                **n,
                "reason": (
                    "All prerequisites complete — a core must-have next step"
                    if n.get("priority") == "must_have"
                    else "Unlocked and ready to start"
                ),
            })
        return result[:limit]
