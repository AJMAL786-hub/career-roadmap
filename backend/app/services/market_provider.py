"""MarketDataProvider service abstraction.

Demo data today; swap in a real provider (job-postings API, LinkedIn, Naukri
dataset) by implementing MarketDataProvider and registering it in the factory.
Responses are cached in-memory with a TTL.
"""
import time
from abc import ABC, abstractmethod
from typing import Dict

# ------------------------------------------------------------------ demo data
# NOTE: clearly-labelled demo/seed data for local development.
_MARKET_DEMO: Dict[str, dict] = {
    "ai-ml-engineer": {
        "salary_ranges": {
            "entry": {"india": "6-12 LPA", "chennai": "5.5-10 LPA", "bangalore": "8-15 LPA",
                      "hyderabad": "7-13 LPA", "pune": "6.5-12 LPA", "mumbai": "7-14 LPA",
                      "delhi_ncr": "7-14 LPA", "remote": "8-20 LPA"},
            "mid": {"india": "14-28 LPA", "chennai": "12-24 LPA", "bangalore": "18-35 LPA",
                    "hyderabad": "16-30 LPA", "pune": "14-26 LPA", "mumbai": "15-28 LPA",
                    "delhi_ncr": "15-30 LPA", "remote": "20-45 LPA"},
            "senior": {"india": "30-60 LPA", "chennai": "25-50 LPA", "bangalore": "35-70 LPA",
                       "hyderabad": "30-60 LPA", "pune": "28-55 LPA", "mumbai": "30-58 LPA",
                       "delhi_ncr": "32-65 LPA", "remote": "40-90 LPA"},
        },
        "hiring_demand_index": 92,
        "demand_trend": [
            {"month": "Mar", "index": 74}, {"month": "Apr", "index": 78},
            {"month": "May", "index": 81}, {"month": "Jun", "index": 84},
            {"month": "Jul", "index": 88}, {"month": "Aug", "index": 92},
        ],
        "top_companies": ["Google", "Microsoft", "Amazon", "Freshworks", "Zoho",
                          "TCS", "Infosys", "Fractal Analytics", "Mu Sigma", "Swiggy"],
        "most_requested_skills": [
            {"skill": "Python", "pct": 88}, {"skill": "Machine Learning", "pct": 76},
            {"skill": "PyTorch", "pct": 54}, {"skill": "LLMs & RAG", "pct": 49},
            {"skill": "SQL", "pct": 47}, {"skill": "AWS", "pct": 44},
            {"skill": "Docker", "pct": 41}, {"skill": "MLOps", "pct": 33},
        ],
        "emerging_skills": ["LLMs & RAG", "Vector Databases", "AI Agents", "MLOps"],
        "declining_skills": ["Classic SAS Modeling", "Manual Feature Scaling"],
        "experience_requirements": [
            {"level": "0-2 years", "share": 28}, {"level": "2-4 years", "share": 34},
            {"level": "4-7 years", "share": 24}, {"level": "7+ years", "share": 14},
        ],
    },
    "data-scientist": {
        "salary_ranges": {
            "entry": {"india": "5-10 LPA", "chennai": "5-9 LPA", "bangalore": "7-13 LPA",
                      "hyderabad": "6-11 LPA", "pune": "6-10 LPA", "mumbai": "6-11 LPA",
                      "delhi_ncr": "6-12 LPA", "remote": "7-15 LPA"},
            "mid": {"india": "12-25 LPA", "chennai": "10-20 LPA", "bangalore": "15-30 LPA",
                    "hyderabad": "13-26 LPA", "pune": "12-22 LPA", "mumbai": "13-24 LPA",
                    "delhi_ncr": "13-26 LPA", "remote": "18-38 LPA"},
            "senior": {"india": "26-55 LPA", "chennai": "22-45 LPA", "bangalore": "30-65 LPA",
                       "hyderabad": "26-52 LPA", "pune": "24-48 LPA", "mumbai": "26-50 LPA",
                       "delhi_ncr": "28-55 LPA", "remote": "35-75 LPA"},
        },
        "hiring_demand_index": 85,
        "demand_trend": [
            {"month": "Mar", "index": 70}, {"month": "Apr", "index": 73},
            {"month": "May", "index": 76}, {"month": "Jun", "index": 79},
            {"month": "Jul", "index": 82}, {"month": "Aug", "index": 85},
        ],
        "top_companies": ["American Express", "Walmart Labs", "Flipkart", "Paytm",
                          "Razorpay", "Zoho", "Freshworks", "LatentView", "Tiger Analytics"],
        "most_requested_skills": [
            {"skill": "Python", "pct": 90}, {"skill": "SQL", "pct": 84},
            {"skill": "Statistics", "pct": 72}, {"skill": "Machine Learning", "pct": 68},
            {"skill": "Tableau", "pct": 44}, {"skill": "A/B Testing", "pct": 38},
            {"skill": "Spark", "pct": 31}, {"skill": "Cloud (AWS/GCP)", "pct": 29},
        ],
        "emerging_skills": ["Causal Inference", "LLMs & RAG", "Feature Stores"],
        "declining_skills": ["Legacy BI Reporting", "SAS"],
        "experience_requirements": [
            {"level": "0-2 years", "share": 30}, {"level": "2-4 years", "share": 36},
            {"level": "4-7 years", "share": 22}, {"level": "7+ years", "share": 12},
        ],
    },
    "full-stack-developer": {
        "salary_ranges": {
            "entry": {"india": "4-9 LPA", "chennai": "4-8 LPA", "bangalore": "6-12 LPA",
                      "hyderabad": "5-10 LPA", "pune": "5-9 LPA", "mumbai": "5-10 LPA",
                      "delhi_ncr": "5-11 LPA", "remote": "6-14 LPA"},
            "mid": {"india": "10-22 LPA", "chennai": "9-18 LPA", "bangalore": "14-28 LPA",
                    "hyderabad": "12-24 LPA", "pune": "11-20 LPA", "mumbai": "12-22 LPA",
                    "delhi_ncr": "12-24 LPA", "remote": "16-35 LPA"},
            "senior": {"india": "24-50 LPA", "chennai": "20-42 LPA", "bangalore": "28-60 LPA",
                       "hyderabad": "24-50 LPA", "pune": "22-45 LPA", "mumbai": "24-48 LPA",
                       "delhi_ncr": "25-52 LPA", "remote": "32-70 LPA"},
        },
        "hiring_demand_index": 95,
        "demand_trend": [
            {"month": "Mar", "index": 80}, {"month": "Apr", "index": 84},
            {"month": "May", "index": 86}, {"month": "Jun", "index": 89},
            {"month": "Jul", "index": 93}, {"month": "Aug", "index": 95},
        ],
        "top_companies": ["Zoho", "Freshworks", "Chargebee", "Kissflow", "TCS",
                          "Infosys", "Wipro", "Swiggy", "Zerodha", "Razorpay"],
        "most_requested_skills": [
            {"skill": "React", "pct": 78}, {"skill": "Node.js", "pct": 71},
            {"skill": "TypeScript", "pct": 62}, {"skill": "SQL", "pct": 58},
            {"skill": "REST APIs", "pct": 66}, {"skill": "AWS", "pct": 46},
            {"skill": "Docker", "pct": 39}, {"skill": "System Design", "pct": 34},
        ],
        "emerging_skills": ["Next.js", "Edge Computing", "tRPC", "Bun"],
        "declining_skills": ["jQuery", "AngularJS"],
        "experience_requirements": [
            {"level": "0-2 years", "share": 34}, {"level": "2-4 years", "share": 38},
            {"level": "4-7 years", "share": 19}, {"level": "7+ years", "share": 9},
        ],
    },
    "devops-engineer": {
        "salary_ranges": {
            "entry": {"india": "5-10 LPA", "chennai": "4.5-9 LPA", "bangalore": "6-12 LPA",
                      "hyderabad": "5.5-11 LPA", "pune": "5-10 LPA", "mumbai": "5.5-10 LPA",
                      "delhi_ncr": "5.5-11 LPA", "remote": "7-15 LPA"},
            "mid": {"india": "12-26 LPA", "chennai": "10-22 LPA", "bangalore": "16-32 LPA",
                    "hyderabad": "14-28 LPA", "pune": "13-25 LPA", "mumbai": "13-25 LPA",
                    "delhi_ncr": "14-27 LPA", "remote": "18-40 LPA"},
            "senior": {"india": "28-58 LPA", "chennai": "24-48 LPA", "bangalore": "32-68 LPA",
                       "hyderabad": "28-56 LPA", "pune": "26-52 LPA", "mumbai": "27-54 LPA",
                       "delhi_ncr": "29-58 LPA", "remote": "38-80 LPA"},
        },
        "hiring_demand_index": 89,
        "demand_trend": [
            {"month": "Mar", "index": 76}, {"month": "Apr", "index": 79},
            {"month": "May", "index": 82}, {"month": "Jun", "index": 84},
            {"month": "Jul", "index": 87}, {"month": "Aug", "index": 89},
        ],
        "top_companies": ["Amazon", "Microsoft", "Zoho", "Freshworks", "PayPal",
                          "Standard Chartered GBS", "Accenture", "Deloitte", "Zerodha"],
        "most_requested_skills": [
            {"skill": "AWS", "pct": 82}, {"skill": "Kubernetes", "pct": 68},
            {"skill": "Terraform", "pct": 61}, {"skill": "CI/CD", "pct": 74},
            {"skill": "Docker", "pct": 77}, {"skill": "Linux", "pct": 70},
            {"skill": "Monitoring & Observability", "pct": 43}, {"skill": "Python", "pct": 52},
        ],
        "emerging_skills": ["Platform Engineering", "GitOps", "FinOps", "eBPF Observability"],
        "declining_skills": ["Chef", "Puppet"],
        "experience_requirements": [
            {"level": "0-2 years", "share": 18}, {"level": "2-4 years", "share": 37},
            {"level": "4-7 years", "share": 30}, {"level": "7+ years", "share": 15},
        ],
    },
    "cybersecurity-analyst": {
        "salary_ranges": {
            "entry": {"india": "4-8 LPA", "chennai": "4-7.5 LPA", "bangalore": "5-10 LPA",
                      "hyderabad": "4.5-9 LPA", "pune": "4.5-8.5 LPA", "mumbai": "5-9 LPA",
                      "delhi_ncr": "5-9.5 LPA", "remote": "6-12 LPA"},
            "mid": {"india": "9-20 LPA", "chennai": "8-17 LPA", "bangalore": "12-24 LPA",
                    "hyderabad": "10-21 LPA", "pune": "9-19 LPA", "mumbai": "10-20 LPA",
                    "delhi_ncr": "10-21 LPA", "remote": "14-30 LPA"},
            "senior": {"india": "20-45 LPA", "chennai": "18-38 LPA", "bangalore": "25-52 LPA",
                       "hyderabad": "22-46 LPA", "pune": "20-42 LPA", "mumbai": "22-44 LPA",
                       "delhi_ncr": "23-47 LPA", "remote": "30-60 LPA"},
        },
        "hiring_demand_index": 87,
        "demand_trend": [
            {"month": "Mar", "index": 75}, {"month": "Apr", "index": 78},
            {"month": "May", "index": 81}, {"month": "Jun", "index": 83},
            {"month": "Jul", "index": 85}, {"month": "Aug", "index": 87},
        ],
        "top_companies": ["Deloitte", "EY", "KPMG", "IBM Security", "Standard Chartered",
                          "PayPal", "Optiv", "Cisco", "Palo Alto Networks", "TCS"],
        "most_requested_skills": [
            {"skill": "SIEM", "pct": 71}, {"skill": "Network Security", "pct": 64},
            {"skill": "Incident Response", "pct": 58}, {"skill": "Vulnerability Assessment", "pct": 52},
            {"skill": "OWASP Top 10", "pct": 47}, {"skill": "Cloud Security", "pct": 41},
            {"skill": "Penetration Testing", "pct": 38}, {"skill": "IAM", "pct": 33},
        ],
        "emerging_skills": ["Cloud Security (CSPM)", "Zero Trust Architecture", "SOAR Automation"],
        "declining_skills": ["Perimeter-only Firewalls", "Legacy Antivirus Management"],
        "experience_requirements": [
            {"level": "0-2 years", "share": 26}, {"level": "2-4 years", "share": 35},
            {"level": "4-7 years", "share": 26}, {"level": "7+ years", "share": 13},
        ],
    },
}

LOCATIONS = ["india", "chennai", "bangalore", "hyderabad", "pune", "mumbai", "delhi_ncr", "remote"]


class MarketDataProvider(ABC):
    @abstractmethod
    def get_market(self, career_slug: str) -> dict:
        ...


class DemoMarketProvider(MarketDataProvider):
    """Seed/demo data provider — replace with a real data source in production."""

    def get_market(self, career_slug: str) -> dict:
        data = _MARKET_DEMO.get(career_slug)
        if not data:
            return {}
        return {**data, "is_demo_data": True}


class CachedMarketService:
    """Caches provider responses with TTL so dashboards stay fast."""

    def __init__(self, provider: MarketDataProvider, ttl_seconds: int = 3600):
        self.provider = provider
        self.ttl = ttl_seconds
        self._cache: Dict[str, tuple] = {}

    def get_market(self, career_slug: str) -> dict:
        now = time.time()
        cached = self._cache.get(career_slug)
        if cached and now - cached[0] < self.ttl:
            return cached[1]
        data = self.provider.get_market(career_slug)
        self._cache[career_slug] = (now, data)
        return data


market_service = CachedMarketService(DemoMarketProvider())
