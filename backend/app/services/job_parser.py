"""JobParser service.

Parses raw job-description text into structured requirements using a layered
strategy:
  1. exact matching against known skill names
  2. alias table lookup (SkillNormalizer)
  3. phrase/rule matching with regexes (experience, education, certifications)
  4. fuzzy token-overlap fallback ("semantic-lite")
  5. optional LLM enrichment when OPENAI_API_KEY is configured (never required)

Business logic lives here, not in route handlers.
"""
import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.services import normalizer


@dataclass
class ExtractedSkill:
    raw: str
    canonical: str
    requirement_type: str = "required"  # required | preferred
    frequency: int = 1
    category: str = "technical"
    matched_skill_id: Optional[int] = None
    match_method: str = "exact"  # exact | alias | rule | fuzzy | llm


@dataclass
class ParsedJob:
    title: str = ""
    skills: List[ExtractedSkill] = field(default_factory=list)
    years_experience: Optional[int] = None
    education: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)


# ---------------------------------------------------------------- category rules
CATEGORY_RULES: List[tuple] = [
    # (category, keywords that hint the mention belongs to this bucket)
    ("programming", ["python", "java", "javascript", "typescript", "golang", "go",
                     "rust", "c++", "c#", "scala", "r programming", "bash"]),
    ("framework", ["react", "next.js", "django", "flask", "fastapi", "spring boot",
                   "node.js", "express", "tensorflow", "pytorch", "scikit-learn",
                   "redux", "tailwind css", "graphql"]),
    ("cloud", ["aws", "azure", "google cloud", "kubernetes", "docker", "terraform",
               "serverless", "lambda"]),
    ("database", ["sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
                  "snowflake", "bigquery", "nosql", "dynamodb"]),
    ("tool", ["git", "jenkins", "ansible", "airflow", "kafka", "spark", "tableau",
              "power bi", "excel", "jira", "figma", "postman", "siem", "splunk"]),
    ("soft_skill", ["communication", "teamwork", "leadership", "problem solving",
                    "mentorship", "collaboration", "presentation", "stakeholder"]),
]

SOFT_SKILL_PATTERNS = [
    r"\bcommunication skills?\b", r"\bteamwork\b", r"\bcollaboration\b",
    r"\bleadership\b", r"\bproblem[- ]solving\b", r"\banalytical (?:skills|thinking)\b",
    r"\bcritical thinking\b", r"\bmentoring\b", r"\bpresentation skills?\b",
    r"\bstakeholder management\b", r"\btime management\b", r"\badaptability\b",
    r"\battention to detail\b",
]

EDUCATION_PATTERNS = [
    (r"\bb\.?tech\b|\bbachelor(?:'s)?(?: of)? (?:technology|engineering)|\bb\.?e\.?\b.*engineering|\bbachelor(?:'s)? degree\b", "Bachelor's degree"),
    (r"\bm\.?tech\b|\bmaster(?:'s)?(?: of)? (?:technology|science)|\bm\.?s\.?c?\b.*\b(computer|data|machine)", "Master's degree"),
    (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
    (r"\bany (?:graduate|degree)\b", "Any graduate degree"),
]

CERTIFICATION_PATTERNS = [
    (r"\baws certified[\w\s,-]*", "AWS Certification"),
    (r"\bazure certification[\w\s,-]*|\baz-\d+[\w\s-]*", "Azure Certification"),
    (r"\bgcp certifi[\w\s,-]*|\bgoogle cloud certifi[\w\s,-]*", "GCP Certification"),
    (r"\bckas?\b|\bcertified kubernetes[\w\s-]*", "Certified Kubernetes"),
    (r"\bcissp\b", "CISSP"),
    (r"\bceh\b|\bcertified ethical hacker\b", "CEH"),
    (r"\bsecurity\+\b", "Security+"),
    (r"\bcomptia[\w\s+-]*", "CompTIA Certification"),
    (r"\bpmp\b", "PMP"),
    (r"\btensorflow developer certificate\b", "TensorFlow Developer Certificate"),
]

DOMAIN_KEYWORDS = [
    "fintech", "finance", "banking", "healthcare", "e-commerce", "ecommerce",
    "retail", "telecom", "insurance", "logistics", "manufacturing", "edtech",
    "saas", "adtech", "gaming", "travel", "energy", "automotive",
]

EXPERIENCE_PATTERN = re.compile(
    r"(\d{1,2})\s*\+?\s*(?:to\s*(\d{1,2})\s*)?(?:-|to)?\s*(\d{1,2})?\s*years?"
    r"|minimum of (\d{1,2}) years?", re.IGNORECASE
)

# Section hints for required vs preferred classification
PREFERRED_SECTION_HINTS = [
    "nice to have", "preferred qualifications", "preferred skills", "bonus points",
    "good to have", "plus:", "desirable", "additional skills",
]
REQUIRED_SECTION_HINTS = [
    "requirements", "required skills", "must have", "what you'll need",
    "qualifications", "you have", "skills required", "mandatory",
]


class JobParser:
    """Stateless parser; call parse() per job description."""

    def __init__(self, known_skill_names: Optional[List[str]] = None):
        # lowercase canonical names of all known skills (from DB) for exact match
        self.known_skills = [normalizer.clean_text(s) for s in (known_skill_names or [])]
        self._known_lookup = {normalizer.normalize_skill_name(s): s for s in self.known_skills}

    # ------------------------------------------------------------- helpers
    def _split_sections(self, text: str):
        """Split JD into (required_text, preferred_text). Preferred defaults empty."""
        lower = text.lower()
        preferred_start = len(text)
        for hint in PREFERRED_SECTION_HINTS:
            idx = lower.find(hint)
            if idx != -1:
                preferred_start = min(preferred_start, idx)
        required_part = text[:preferred_start]
        preferred_part = text[preferred_start:] if preferred_start < len(text) else ""
        return required_part, preferred_part

    def _infer_category(self, canonical: str) -> str:
        for category, keywords in CATEGORY_RULES:
            if any(k == canonical or k in canonical for k in keywords):
                return category
        return "technical"

    def _match_known(self, canonical: str) -> Optional[str]:
        """Return the known-skill name this canonical maps to, else None."""
        if canonical in self._known_lookup:
            return self._known_lookup[canonical]
        # plural/singular tolerance
        if canonical.endswith("s") and canonical[:-1] in self._known_lookup:
            return self._known_lookup[canonical[:-1]]
        return None

    # ------------------------------------------------------------- parsing
    def parse(self, text: str) -> ParsedJob:
        parsed = ParsedJob()
        required_part, preferred_part = self._split_sections(text)

        # --- experience ---
        m = EXPERIENCE_PATTERN.search(text)
        if m:
            groups = [g for g in m.groups() if g]
            if groups:
                try:
                    parsed.years_experience = int(groups[0])
                except ValueError:
                    pass

        # --- education ---
        lower = text.lower()
        for pattern, label in EDUCATION_PATTERNS:
            if re.search(pattern, lower) and label not in parsed.education:
                parsed.education.append(label)

        # --- certifications ---
        for pattern, label in CERTIFICATION_PATTERNS:
            if re.search(pattern, lower) and label not in parsed.certifications:
                parsed.certifications.append(label)

        # --- soft skills ---
        for pattern in SOFT_SKILL_PATTERNS:
            m = re.search(pattern, lower)
            if m:
                val = normalizer.clean_text(m.group(0))
                if val not in parsed.soft_skills:
                    parsed.soft_skills.append(val)

        # --- domains ---
        for kw in DOMAIN_KEYWORDS:
            if kw in lower and kw not in parsed.domains:
                parsed.domains.append(kw)

        # --- skills: layered extraction ---
        skill_hits: Dict[str, ExtractedSkill] = {}

        def add_hit(raw: str, method: str, requirement_type: str):
            canonical = normalizer.normalize_skill_name(raw)
            if not canonical or len(canonical) < 2:
                return
            existing = skill_hits.get(canonical)
            if existing:
                existing.frequency += 1
                if requirement_type == "required":
                    existing.requirement_type = "required"
                return
            category = self._infer_category(canonical)
            skill_hits[canonical] = ExtractedSkill(
                raw=raw.strip(), canonical=canonical,
                requirement_type=requirement_type, frequency=1,
                category=category, match_method=method,
            )

        # Layer 1+2+3: scan alias/canonical vocabulary over both sections
        vocab = sorted(normalizer.ALIAS_MAP.keys() | set(
            a for aliases in normalizer.ALIAS_MAP.values() for a in aliases
        ), key=len, reverse=True)
        for section_text, req_type in ((required_part, "required"), (preferred_part, "preferred")):
            low = normalizer.clean_text(section_text)
            for term in vocab:
                pattern = r"(?<![a-z0-9+#])" + re.escape(term) + r"(?![a-z0-9+#])"
                if re.search(pattern, low):
                    add_hit(term, "alias" if term not in normalizer.ALIAS_MAP else "exact", req_type)

        # Layer 4: fuzzy fallback for capitalized multi-word phrases not yet matched
        for phrase in re.findall(r"\b[A-Z][A-Za-z+#]*(?:[ .][A-Z][A-Za-z+#]*)+\b", text):
            canon = normalizer.normalize_skill_name(phrase)
            if canon in skill_hits or len(canon) < 4:
                continue
            fuzzy = normalizer.best_fuzzy_match(canon, list(self._known_lookup.keys()), threshold=0.75)
            if fuzzy:
                add_hit(fuzzy[0], "fuzzy", "preferred")

        parsed.skills = list(skill_hits.values())
        return parsed

    # ------------------------------------------------------- optional LLM hook
    def enrich_with_llm(self, parsed: ParsedJob, text: str) -> ParsedJob:
        """Optional LLM enrichment. Activates only when OPENAI_API_KEY is set.
        The application never depends on this succeeding."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return parsed
        try:
            import urllib.request
            body = json.dumps({
                "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                "messages": [{
                    "role": "user",
                    "content": (
                        "Extract skills from this job description as JSON: "
                        '{"skills": [{"name": str, "type": "required"|"preferred"}], '
                        '"years_experience": int|null}. Text:\n' + text[:6000]
                    ),
                }],
                "temperature": 0,
            }).encode()
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions", data=body,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {api_key}"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
            content = data["choices"][0]["message"]["content"]
            content = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()
            extra = json.loads(content)
            seen = {s.canonical for s in parsed.skills}
            for item in extra.get("skills", []):
                canon = normalizer.normalize_skill_name(item.get("name", ""))
                if canon and canon not in seen:
                    seen.add(canon)
                    parsed.skills.append(ExtractedSkill(
                        raw=item.get("name", canon), canonical=canon,
                        requirement_type=item.get("type", "required"),
                        category=self._infer_category(canon), match_method="llm",
                    ))
            if extra.get("years_experience") and not parsed.years_experience:
                parsed.years_experience = int(extra["years_experience"])
        except Exception:
            pass  # never fail the analysis because of the optional LLM
        return parsed
