"""SkillNormalizer service.

Normalizes free-text skill mentions into canonical skill names.
Layered approach:
  1. exact canonical-name match
  2. alias table lookup
  3. phrase/rule based cleanup (e.g. "Python 3" -> "python", "K8s" -> "kubernetes")
  4. fuzzy token-overlap matching (lightweight semantic fallback)

An optional LLM-based normalizer can be plugged in via environment config,
but the app never depends on it.
"""
import re
from typing import Dict, List, Optional, Tuple

# Canonical name -> aliases. Keys are lowercase canonical names.
ALIAS_MAP: Dict[str, List[str]] = {
    "python": ["python 3", "python programming", "python3", "py"],
    "javascript": ["js", "javascript es6", "es6", "vanilla javascript", "javascript (es6+)"],
    "typescript": ["ts"],
    "java": ["core java", "java 8", "java se"],
    "go": ["golang"],
    "rust": [],
    "c++": ["cpp", "c plus plus"],
    "c#": ["csharp", "c sharp", ".net c#"],
    "sql": ["structured query language", "sql queries", "advanced sql"],
    "nosql": ["no sql"],
    "postgresql": ["postgres", "psql", "postgresql db"],
    "mysql": ["my sql"],
    "mongodb": ["mongo", "mongo db"],
    "redis": [],
    "sqlite": [],
    "elasticsearch": ["elastic search", "opensearch"],
    "snowflake": [],
    "bigquery": ["google bigquery"],
    "spark": ["apache spark", "pyspark"],
    "hadoop": ["apache hadoop"],
    "kafka": ["apache kafka"],
    "airflow": ["apache airflow"],
    "dbt": ["data build tool"],
    "machine learning": ["ml", "machine learning algorithms", "applied machine learning", "classical ml"],
    "deep learning": ["dl", "neural networks", "artificial neural networks"],
    "natural language processing": ["nlp", "text processing"],
    "computer vision": ["cv", "image processing"],
    "reinforcement learning": ["rl"],
    "mlops": ["ml ops", "machine learning operations", "mlo ps"],
    "llms & rag": ["large language models", "llm", "rag", "retrieval augmented generation",
                   "generative ai", "genai", "gen ai", "llm fine-tuning", "prompt engineering"],
    "transformers": ["transformer models", "hugging face transformers", "bert", "gpt"],
    "pytorch": ["torch", "pytorch lightning"],
    "tensorflow": ["tf", "keras", "tensorflow 2"],
    "scikit-learn": ["sklearn", "scikit learn"],
    "numpy": [],
    "pandas": [],
    "matplotlib": [],
    "seaborn": [],
    "statistics": ["statistics & probability", "probability & statistics", "statistical analysis",
                   "probability", "inferential statistics"],
    "data visualization": ["data viz", "dataviz", "visualisation"],
    "tableau": [],
    "power bi": ["powerbi", "power-bi"],
    "excel": ["microsoft excel", "advanced excel"],
    "a/b testing": ["ab testing", "experimentation", "a/b experiments"],
    "feature engineering": [],
    "model deployment": ["model serving", "model deployment & monitoring"],
    "docker": ["containerization", "containers", "docker compose", "container orchestration basics"],
    "kubernetes": ["k8s", "kubernetes orchestration", "eks", "aks", "gke"],
    "terraform": ["infrastructure as code", "iac", "terraform cloud"],
    "ansible": [],
    "jenkins": [],
    "ci/cd": ["cicd", "ci cd", "continuous integration", "continuous delivery",
              "continuous integration/delivery", "github actions", "gitlab ci"],
    "aws": ["amazon web services", "aws cloud", "ec2", "s3", "lambda", "aws lambda"],
    "azure": ["microsoft azure"],
    "google cloud": ["gcp", "google cloud platform"],
    "linux": ["linux administration", "unix", "bash/shell scripting", "shell scripting", "bash"],
    "networking": ["computer networks", "tcp/ip", "dns", "network protocols"],
    "git": ["github", "gitlab", "version control", "version control (git)"],
    "monitoring & observability": ["observability", "monitoring", "prometheus", "grafana",
                                   "datadog", "application monitoring"],
    "security fundamentals": ["information security", "infosec", "cyber security", "cybersecurity basics"],
    "owasp top 10": ["owasp", "owasp top ten"],
    "penetration testing": ["pentesting", "ethical hacking", "pen test"],
    "incident response": ["soc operations", "security incident response"],
    "siem": ["splunk", "security information and event management", "qradar"],
    "cryptography": ["encryption", "applied cryptography"],
    "vulnerability assessment": ["vulnerability scanning", "nessus", "qualys"],
    "cloud security": ["cloud security posture"],
    "identity & access management": ["iam", "access management", "active directory"],
    "html": ["html5"],
    "css": ["css3", "modern css"],
    "react": ["react.js", "reactjs", "react js", "react 18"],
    "next.js": ["nextjs", "next js"],
    "node.js": ["nodejs", "node js", "express", "express.js", "expressjs"],
    "rest apis": ["restful api development", "rest api development", "rest api", "restful apis",
                  "restful web services", "api development", "restful api design"],
    "graphql": [],
    "redux": ["redux toolkit"],
    "tailwind css": ["tailwind", "tailwindcss"],
    "fastapi": ["fast api"],
    "django": ["django rest framework", "drf"],
    "flask": [],
    "spring boot": ["spring", "springboot"],
    "microservices": ["microservices architecture", "micro-service architecture"],
    "system design": ["system architecture", "distributed systems", "scalable system design"],
    "testing": ["unit testing", "automated testing", "test automation", "jest", "pytest"],
    "accessibility": ["a11y", "web accessibility"],
    "agile": ["agile methodologies", "agile development"],
    "scrum": ["scrum framework"],
    "communication": ["communication skills", "verbal communication", "written communication"],
    "problem solving": ["analytical thinking", "analytical skills", "critical thinking"],
    "teamwork": ["collaboration", "cross-functional collaboration"],
    "mentorship": ["mentoring", "mentoring junior engineers"],
}

# Reverse lookup: alias -> canonical (lowercase)
_ALIAS_TO_CANONICAL: Dict[str, str] = {}
for _canon, _aliases in ALIAS_MAP.items():
    _ALIAS_TO_CANONICAL[_canon] = _canon
    for _a in _aliases:
        _ALIAS_TO_CANONICAL[_a] = _canon

_WORD_SPLIT = re.compile(r"[^a-z0-9+#./]+")


def clean_text(text: str) -> str:
    """Lowercase and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


def normalize_skill_name(name: str) -> str:
    """Return the canonical lowercase name for a raw skill mention."""
    key = clean_text(name)
    if not key:
        return ""
    # Layer 1+2: exact / alias table
    if key in _ALIAS_TO_CANONICAL:
        return _ALIAS_TO_CANONICAL[key]
    # Layer 3: rule-based cleanup
    stripped = re.sub(r"\b\d+(\.\d+)?\b", "", key)  # versions: python 3, react 18
    stripped = re.sub(r"\b(programming|development|skills?|framework|library|orchestration|basics?)\b", "", stripped)
    stripped = clean_text(stripped)
    if stripped in _ALIAS_TO_CANONICAL:
        return _ALIAS_TO_CANONICAL[stripped]
    # possessives/plurals
    if stripped.endswith("s") and stripped[:-1] in _ALIAS_TO_CANONICAL:
        return _ALIAS_TO_CANONICAL[stripped[:-1]]
    return key


def canonical_key(name: str) -> str:
    """Unified comparison key: normalized name collapsed to kebab-case.

    Guarantees 'CI/CD', 'ci cd' and the seeded slug 'ci-cd' all agree.
    """
    base = normalize_skill_name(name)
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")


def token_overlap(a: str, b: str) -> float:
    """Jaccard similarity between two strings' word tokens."""
    ta = set(t for t in _WORD_SPLIT.split(a) if t)
    tb = set(t for t in _WORD_SPLIT.split(b) if t)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def best_fuzzy_match(name: str, candidates: List[str], threshold: float = 0.6) -> Optional[Tuple[str, float]]:
    """Layer 4 fallback: closest candidate by token overlap."""
    key = clean_text(name)
    best: Optional[Tuple[str, float]] = None
    for cand in candidates:
        score = token_overlap(key, cand)
        if score >= threshold and (best is None or score > best[1]):
            best = (cand, score)
    return best
