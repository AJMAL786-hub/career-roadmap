"""GapAnalyzer + RecommendationEngine services.

Gap analysis compares parsed job requirements against the user's skill state
and produces prioritized "learn these first" recommendations.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.services.job_parser import ParsedJob
from app.services.normalizer import canonical_key


@dataclass
class GapItem:
    canonical: str
    display_name: str
    requirement_type: str          # required | preferred
    category: str = "technical"
    user_status: str = "not_started"   # not_started | in_progress | completed
    confidence: int = 0                # 0-5
    frequency: int = 1                 # mentions in the JD
    matched_skill_id: Optional[int] = None
    estimated_hours: float = 8.0
    priority_score: float = 0.0
    priority_label: str = "Medium"     # Critical | High | Medium | Low


@dataclass
class GapReport:
    exact_matches: List[GapItem] = field(default_factory=list)
    partial_matches: List[GapItem] = field(default_factory=list)
    missing_required: List[GapItem] = field(default_factory=list)
    missing_preferred: List[GapItem] = field(default_factory=list)
    overqualified: List[GapItem] = field(default_factory=list)  # user has, JD doesn't ask
    match_score: float = 0.0        # 0-100 weighted coverage of required skills
    learn_first: List[GapItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "exact_matches": [g.__dict__ for g in self.exact_matches],
            "partial_matches": [g.__dict__ for g in self.partial_matches],
            "missing_required": [g.__dict__ for g in self.missing_required],
            "missing_preferred": [g.__dict__ for g in self.missing_preferred],
            "overqualified": [g.__dict__ for g in self.overqualified],
            "match_score": self.match_score,
            "learn_first": [g.__dict__ for g in self.learn_first],
        }


# Weights for priority score computation
W_FREQUENCY = 2.0        # per mention in JD (capped)
W_REQUIRED_BONUS = 30.0  # required beats preferred
W_CAREER_RELEVANCE = {"must_have": 25.0, "recommended": 12.0, "optional": 4.0}
W_USER_PROFICIENCY = -6.0  # per confidence point; in-progress reduces urgency
W_EFFORT_PENALTY = -0.35   # per estimated hour (quick wins rank higher)


def _priority_label(score: float) -> str:
    if score >= 55:
        return "Critical"
    if score >= 38:
        return "High"
    if score >= 22:
        return "Medium"
    return "Low"


def compute_priority(item: GapItem, career_priority: str) -> float:
    """Priority score from frequency, requirement status, career relevance,
    user proficiency and learning effort."""
    score = min(item.frequency, 5) * W_FREQUENCY
    if item.requirement_type == "required":
        score += W_REQUIRED_BONUS
    else:
        score += W_REQUIRED_BONUS * 0.35
    score += W_CAREER_RELEVANCE.get(career_priority, 12.0)
    if item.user_status == "in_progress":
        score += W_USER_PROFICIENCY * max(item.confidence, 1)
    elif item.user_status == "completed":
        score += W_USER_PROFICIENCY * 5
    score += W_EFFORT_PENALTY * min(item.estimated_hours, 120)
    return round(max(score, 0), 1)


class GapAnalyzer:
    """Compares a ParsedJob against the user's skill map.

    user_skill_map: canonical(lower) -> {status, confidence, skill_id, name}
    career_skill_map: canonical(lower) -> {skill_id, priority, hours, name}
    """

    def analyze(
        self,
        parsed: ParsedJob,
        user_skill_map: Dict[str, dict],
        career_skill_map: Dict[str, dict],
    ) -> GapReport:
        report = GapReport()
        total_required = 0
        covered_required = 0.0

        for es in parsed.skills:
            key = canonical_key(es.canonical) or es.canonical
            user_state = user_skill_map.get(key)
            career_meta = career_skill_map.get(key, {})

            item = GapItem(
                canonical=key,
                display_name=career_meta.get("name") or es.raw.title(),
                requirement_type=es.requirement_type,
                category=es.category,
                frequency=es.frequency,
                matched_skill_id=(user_state or {}).get("skill_id") or career_meta.get("skill_id"),
                estimated_hours=float(career_meta.get("hours", 8)),
            )
            if user_state:
                item.user_status = user_state["status"]
                item.confidence = user_state.get("confidence", 0)

            # Career relevance for scoring
            career_priority = career_meta.get("priority", "recommended")
            # A JD-required skill the target career marks optional is still
            # soft: it must not block readiness or deflate the match score.
            is_hard_requirement = (
                es.requirement_type == "required"
                and career_priority not in ("optional", "nice_to_have")
            )

            if item.user_status == "completed":
                report.exact_matches.append(item)
                if is_hard_requirement:
                    covered_required += 1.0
                    total_required += 1
                    continue
            elif item.user_status == "in_progress":
                report.partial_matches.append(item)
                if is_hard_requirement:
                    # counts toward the denominator but earns no coverage
                    # until completed (strict readiness scoring)
                    total_required += 1
                    continue
            else:
                if is_hard_requirement:
                    report.missing_required.append(item)
                    total_required += 1
                elif es.requirement_type == "preferred":
                    report.missing_preferred.append(item)
                # else: JD-required but career-optional -> not a real gap

            item.priority_score = compute_priority(item, career_priority)
            item.priority_label = _priority_label(item.priority_score)

        # Overqualified: completed skills not requested by this JD
        requested_keys = {canonical_key(es.canonical) for es in parsed.skills}
        for raw_key, meta in user_skill_map.items():
            key = canonical_key(raw_key)
            if meta["status"] == "completed" and key not in requested_keys:
                report.overqualified.append(GapItem(
                    canonical=key,
                    display_name=meta.get("name", key.title()),
                    requirement_type="required",
                    category="technical",
                    user_status="completed",
                    matched_skill_id=meta.get("skill_id"),
                ))

        report.match_score = round(
            (covered_required / total_required * 100) if total_required else 0.0, 1
        )

        # Ranked "learn these first": missing required by score desc, then preferred
        ranked = sorted(
            report.missing_required + report.missing_preferred,
            key=lambda g: g.priority_score, reverse=True,
        )
        report.learn_first = ranked[:10]
        return report
