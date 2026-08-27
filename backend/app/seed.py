"""Seed database with 5 career paths and their full skill DAGs."""
import re
from app.database import SessionLocal, init_db
from app.models.career import CareerPath
from app.models.skill import Skill, SkillAlias, RoadmapNode, RoadmapEdge
from app.models.learning import LearningResource


def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


# ---------- career definitions ----------

CAREERS = [
    {
        "title": "AI/ML Engineer",
        "slug": "ai-ml-engineer",
        "description": "Design and deploy machine learning models, build AI pipelines, and integrate intelligent systems into production applications.",
        "icon": "brain",
        "color": "#8b5cf6",
        "skills": [
            # Fundamentals
            {"name": "Python", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 40,
             "desc": "Core programming language for AI/ML development.", "why": "Python is the lingua franca of machine learning, with the richest ecosystem of libraries.",
             "aliases": ["Python 3", "Python programming", "Py"]},
            {"name": "Mathematics for ML", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 60,
             "desc": "Linear algebra, calculus, probability & statistics.", "why": "Underpins every ML algorithm."},
            {"name": "Data Structures & Algorithms", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 40,
             "desc": "Fundamental CS concepts for efficient data processing.", "why": "Needed for optimizing models and passing technical interviews."},
            {"name": "SQL", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 20,
             "desc": "Query and manage relational databases.", "why": "Essential for extracting training data from databases.",
             "aliases": ["Structured Query Language"]},
            {"name": "NumPy", "level": "fundamental", "category": "framework", "priority": "must_have", "hours": 15,
             "desc": "Numerical computing library for Python.", "why": "Foundation for all scientific computing in Python."},
            {"name": "Pandas", "level": "fundamental", "category": "framework", "priority": "must_have", "hours": 20,
             "desc": "Data manipulation and analysis library.", "why": "Standard tool for data wrangling and exploration."},
            # Intermediate
            {"name": "Machine Learning", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 80,
             "desc": "Supervised, unsupervised, and reinforcement learning algorithms.", "why": "Core competency for any ML engineer.",
             "aliases": ["ML"], "prereqs": ["Python", "Mathematics for ML", "NumPy", "Pandas"]},
            {"name": "Scikit-learn", "level": "intermediate", "category": "framework", "priority": "must_have", "hours": 25,
             "desc": "Machine learning library for classical algorithms.", "why": "Go-to library for classical ML models.",
             "aliases": ["sklearn"], "prereqs": ["Machine Learning"]},
            {"name": "Deep Learning", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 60,
             "desc": "Neural networks, CNNs, RNNs, transformers.", "why": "Powers state-of-the-art AI systems.",
             "aliases": ["DL"], "prereqs": ["Machine Learning"]},
            {"name": "TensorFlow", "level": "intermediate", "category": "framework", "priority": "recommended", "hours": 40,
             "desc": "Google's deep learning framework.", "why": "Widely used in production ML systems.",
             "aliases": ["TF"], "prereqs": ["Deep Learning"]},
            {"name": "PyTorch", "level": "intermediate", "category": "framework", "priority": "recommended", "hours": 40,
             "desc": "Facebook's deep learning framework.", "why": "Preferred for research and increasingly in production.",
             "aliases": ["Torch"], "prereqs": ["Deep Learning"]},
            {"name": "Data Visualization", "level": "intermediate", "category": "technical", "priority": "recommended", "hours": 15,
             "desc": "Matplotlib, Seaborn, Plotly for visualizing data and results.", "why": "Critical for understanding data and communicating findings.",
             "prereqs": ["Pandas"]},
            {"name": "Feature Engineering", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Transforming raw data into meaningful features.", "why": "Often determines model performance more than algorithm choice.",
             "prereqs": ["Machine Learning", "Pandas"]},
            # Advanced
            {"name": "Natural Language Processing", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 50,
             "desc": "Text processing, transformers, LLMs.", "why": "One of the fastest-growing areas in AI.",
             "aliases": ["NLP"], "prereqs": ["Deep Learning"]},
            {"name": "Computer Vision", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 50,
             "desc": "Image classification, object detection, segmentation.", "why": "Powers applications from self-driving cars to medical imaging.",
             "prereqs": ["Deep Learning"]},
            {"name": "MLOps", "level": "advanced", "category": "technical", "priority": "must_have", "hours": 40,
             "desc": "ML model deployment, monitoring, and lifecycle management.", "why": "Bridges the gap between model development and production.",
             "prereqs": ["Machine Learning", "Docker"]},
            {"name": "Docker", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 20,
             "desc": "Containerize ML applications.", "why": "Standard for packaging and deploying ML models.",
             "aliases": ["Containerization"], "prereqs": ["Python"]},
            {"name": "Cloud Platforms", "level": "advanced", "category": "tool", "priority": "recommended", "hours": 30,
             "desc": "AWS SageMaker, GCP Vertex AI, Azure ML.", "why": "Most production ML runs on cloud infrastructure.",
             "aliases": ["AWS", "GCP", "Azure"], "prereqs": ["Docker"]},
            {"name": "Git", "level": "fundamental", "category": "tool", "priority": "must_have", "hours": 10,
             "desc": "Version control for code and experiments.", "why": "Essential for collaboration and experiment tracking.",
             "aliases": ["GitHub"]},
            # Soft skills
            {"name": "Communication", "level": "fundamental", "category": "soft_skill", "priority": "must_have", "hours": 10,
             "desc": "Explain technical concepts to non-technical stakeholders.", "why": "ML engineers must communicate model decisions and limitations."},
            {"name": "Problem Solving", "level": "fundamental", "category": "soft_skill", "priority": "must_have", "hours": 10,
             "desc": "Analytical thinking and structured problem decomposition.", "why": "Core skill for debugging models and designing solutions."},
            # Certification
            {"name": "AWS ML Specialty", "level": "advanced", "category": "certification", "priority": "optional", "hours": 40,
             "desc": "AWS Certified Machine Learning – Specialty certification.", "why": "Validates ML skills on AWS platform.",
             "prereqs": ["Cloud Platforms", "Machine Learning"]},
        ],
    },
    {
        "title": "Data Scientist",
        "slug": "data-scientist",
        "description": "Analyze complex datasets, build predictive models, and derive actionable insights to drive business decisions.",
        "icon": "bar-chart-3",
        "color": "#06b6d4",
        "skills": [
            {"name": "Python", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 40,
             "desc": "Primary programming language for data science.", "why": "Most popular language in data science with unmatched library ecosystem."},
            {"name": "Statistics", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 50,
             "desc": "Descriptive stats, inferential stats, hypothesis testing.", "why": "Foundation of all data analysis and modeling."},
            {"name": "SQL", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Database querying and data extraction.", "why": "Most business data lives in relational databases."},
            {"name": "Pandas", "level": "fundamental", "category": "framework", "priority": "must_have", "hours": 25,
             "desc": "Data manipulation and cleaning.", "why": "Workhorse library for data wrangling."},
            {"name": "NumPy", "level": "fundamental", "category": "framework", "priority": "must_have", "hours": 15,
             "desc": "Numerical computing foundation.", "why": "Underlies Pandas and all scientific computing."},
            {"name": "Data Visualization", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Matplotlib, Seaborn, Plotly, Tableau.", "why": "Communicating insights is half the job of a data scientist.",
             "prereqs": ["Pandas"]},
            {"name": "Machine Learning", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 70,
             "desc": "Classification, regression, clustering algorithms.", "why": "Core skill for predictive modeling.",
             "prereqs": ["Python", "Statistics", "NumPy", "Pandas"]},
            {"name": "Scikit-learn", "level": "intermediate", "category": "framework", "priority": "must_have", "hours": 25,
             "desc": "Primary ML library for data science.", "why": "Industry standard for classical ML.",
             "prereqs": ["Machine Learning"]},
            {"name": "Feature Engineering", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Creating predictive features from raw data.", "why": "Separates good models from great ones.",
             "prereqs": ["Machine Learning", "Pandas"]},
            {"name": "Deep Learning", "level": "intermediate", "category": "technical", "priority": "recommended", "hours": 40,
             "desc": "Neural networks for complex pattern recognition.", "why": "Increasingly important for unstructured data.",
             "prereqs": ["Machine Learning"]},
            {"name": "A/B Testing", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 15,
             "desc": "Experiment design and statistical significance.", "why": "Critical for validating business hypotheses.",
             "prereqs": ["Statistics"]},
            {"name": "Big Data Tools", "level": "intermediate", "category": "tool", "priority": "recommended", "hours": 30,
             "desc": "Spark, Hadoop, Dask for large-scale data processing.", "why": "Required when datasets outgrow single-machine capacity.",
             "prereqs": ["Python", "SQL"]},
            {"name": "NLP", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 40,
             "desc": "Text analytics, sentiment analysis, topic modeling.", "why": "Opens up vast text data sources for analysis.",
             "prereqs": ["Deep Learning"]},
            {"name": "Time Series Analysis", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 25,
             "desc": "Forecasting, trend analysis, ARIMA, Prophet.", "why": "Many business problems are temporal in nature.",
             "prereqs": ["Machine Learning", "Statistics"]},
            {"name": "Cloud Platforms", "level": "advanced", "category": "tool", "priority": "recommended", "hours": 25,
             "desc": "AWS, GCP, Azure for scalable data processing.", "why": "Production data science requires cloud infrastructure.",
             "prereqs": ["Python"]},
            {"name": "Git", "level": "fundamental", "category": "tool", "priority": "must_have", "hours": 10,
             "desc": "Version control.", "why": "Collaboration and reproducibility."},
            {"name": "Business Acumen", "level": "fundamental", "category": "soft_skill", "priority": "must_have", "hours": 15,
             "desc": "Understanding business context and stakeholder needs.", "why": "Data science exists to solve business problems."},
            {"name": "Storytelling with Data", "level": "intermediate", "category": "soft_skill", "priority": "must_have", "hours": 15,
             "desc": "Presenting insights compellingly.", "why": "Insights without narrative don't drive action.",
             "prereqs": ["Data Visualization"]},
        ],
    },
    {
        "title": "Full Stack Developer",
        "slug": "full-stack-developer",
        "description": "Build end-to-end web applications with modern frontend frameworks, backend APIs, databases, and deployment pipelines.",
        "icon": "code-2",
        "color": "#10b981",
        "skills": [
            {"name": "HTML", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 15,
             "desc": "Structure of web pages.", "why": "The foundation of all web content.", "aliases": ["HTML5"]},
            {"name": "CSS", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Styling and layout, including Flexbox and Grid.", "why": "Controls the visual presentation of web applications.", "aliases": ["CSS3"]},
            {"name": "JavaScript", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 50,
             "desc": "Core programming language of the web.", "why": "Runs in every browser, essential for interactivity.", "aliases": ["JS"],
             "prereqs": ["HTML", "CSS"]},
            {"name": "TypeScript", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Typed superset of JavaScript.", "why": "Catches bugs at compile time, improves code quality.", "aliases": ["TS"],
             "prereqs": ["JavaScript"]},
            {"name": "React", "level": "intermediate", "category": "framework", "priority": "must_have", "hours": 50,
             "desc": "Component-based UI library by Meta.", "why": "Most popular frontend framework with vast ecosystem.", "aliases": ["React.js", "ReactJS"],
             "prereqs": ["JavaScript"]},
            {"name": "Node.js", "level": "intermediate", "category": "framework", "priority": "must_have", "hours": 35,
             "desc": "JavaScript runtime for backend development.", "why": "Enables full-stack JavaScript development.", "aliases": ["NodeJS"],
             "prereqs": ["JavaScript"]},
            {"name": "REST APIs", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 20,
             "desc": "RESTful API design and implementation.", "why": "Standard protocol for client-server communication.",
             "aliases": ["RESTful APIs", "REST API development"], "prereqs": ["Node.js"]},
            {"name": "SQL", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Relational database querying.", "why": "Most applications store data in relational databases."},
            {"name": "PostgreSQL", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 20,
             "desc": "Advanced open-source relational database.", "why": "Production-grade database for web applications.",
             "aliases": ["Postgres"], "prereqs": ["SQL"]},
            {"name": "MongoDB", "level": "intermediate", "category": "tool", "priority": "recommended", "hours": 15,
             "desc": "Document-based NoSQL database.", "why": "Flexible schema for rapidly evolving data.", "aliases": ["Mongo"],
             "prereqs": ["REST APIs"]},
            {"name": "Git", "level": "fundamental", "category": "tool", "priority": "must_have", "hours": 10,
             "desc": "Version control system.", "why": "Essential for collaboration and code management."},
            {"name": "Docker", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 20,
             "desc": "Application containerization.", "why": "Standard for consistent development and deployment environments.",
             "prereqs": ["Node.js"]},
            {"name": "GraphQL", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 20,
             "desc": "Query language for APIs.", "why": "Flexible alternative to REST for complex data fetching.",
             "prereqs": ["REST APIs"]},
            {"name": "Testing", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Unit, integration, and E2E testing.", "why": "Ensures application reliability and prevents regressions.",
             "prereqs": ["React", "Node.js"]},
            {"name": "CI/CD", "level": "advanced", "category": "tool", "priority": "recommended", "hours": 20,
             "desc": "Automated build, test, and deploy pipelines.", "why": "Enables rapid, reliable software delivery.",
             "aliases": ["CICD"], "prereqs": ["Docker", "Git", "Testing"]},
            {"name": "Cloud Deployment", "level": "advanced", "category": "tool", "priority": "recommended", "hours": 25,
             "desc": "Deploy to AWS, GCP, or Azure.", "why": "Production applications need cloud hosting.",
             "prereqs": ["Docker"]},
            {"name": "Redis", "level": "advanced", "category": "tool", "priority": "recommended", "hours": 15,
             "desc": "In-memory data store for caching.", "why": "Dramatically improves application performance.",
             "prereqs": ["REST APIs"]},
            {"name": "Agile", "level": "fundamental", "category": "soft_skill", "priority": "must_have", "hours": 10,
             "desc": "Agile methodologies and Scrum.", "why": "Most development teams use agile practices."},
            {"name": "System Design", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 40,
             "desc": "Designing scalable distributed systems.", "why": "Critical for senior roles and architecture decisions.",
             "prereqs": ["REST APIs", "PostgreSQL", "Docker"]},
        ],
    },
    {
        "title": "DevOps Engineer",
        "slug": "devops-engineer",
        "description": "Automate infrastructure, manage CI/CD pipelines, ensure system reliability, and bridge development and operations.",
        "icon": "settings",
        "color": "#f59e0b",
        "skills": [
            {"name": "Linux", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 40,
             "desc": "Linux system administration, shell scripting.", "why": "Most servers run Linux; foundational for all DevOps work."},
            {"name": "Networking Fundamentals", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "TCP/IP, DNS, HTTP, load balancing.", "why": "Understanding network infrastructure is critical for DevOps."},
            {"name": "Python", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Scripting and automation language.", "why": "Primary language for DevOps tooling and automation."},
            {"name": "Bash Scripting", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 20,
             "desc": "Shell scripting for automation.", "why": "Ubiquitous in automation and system administration.",
             "prereqs": ["Linux"]},
            {"name": "Git", "level": "fundamental", "category": "tool", "priority": "must_have", "hours": 15,
             "desc": "Version control and GitOps workflows.", "why": "Foundation of modern DevOps practices."},
            {"name": "Docker", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 30,
             "desc": "Container runtime and image building.", "why": "Standard for application packaging and deployment.",
             "prereqs": ["Linux"]},
            {"name": "Kubernetes", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 50,
             "desc": "Container orchestration platform.", "why": "Industry standard for running containers at scale.",
             "aliases": ["K8s"], "prereqs": ["Docker", "Networking Fundamentals"]},
            {"name": "CI/CD", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Jenkins, GitHub Actions, GitLab CI pipelines.", "why": "Automates the software delivery lifecycle.",
             "aliases": ["CICD"], "prereqs": ["Git", "Docker"]},
            {"name": "Terraform", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 35,
             "desc": "Infrastructure as Code tool.", "why": "Enables reproducible, version-controlled infrastructure.",
             "prereqs": ["Cloud Platforms"]},
            {"name": "Ansible", "level": "intermediate", "category": "tool", "priority": "recommended", "hours": 25,
             "desc": "Configuration management and automation.", "why": "Agentless automation for server configuration.",
             "prereqs": ["Linux", "Python"]},
            {"name": "Cloud Platforms", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 50,
             "desc": "AWS, GCP, or Azure services.", "why": "DevOps engineers must master at least one cloud provider.",
             "aliases": ["AWS", "GCP", "Azure"], "prereqs": ["Linux", "Networking Fundamentals"]},
            {"name": "Monitoring & Observability", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Prometheus, Grafana, ELK stack, Datadog.", "why": "Visibility into system health is essential for reliability.",
             "prereqs": ["Linux", "Docker"]},
            {"name": "Security", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 20,
             "desc": "DevSecOps, secrets management, scanning.", "why": "Security must be integrated into the CI/CD pipeline.",
             "prereqs": ["CI/CD"]},
            {"name": "Service Mesh", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 25,
             "desc": "Istio, Linkerd for microservice networking.", "why": "Manages complex service-to-service communication.",
             "prereqs": ["Kubernetes"]},
            {"name": "GitOps", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 20,
             "desc": "ArgoCD, Flux for declarative deployments.", "why": "Modern approach to continuous deployment.",
             "prereqs": ["Git", "Kubernetes"]},
            {"name": "Site Reliability Engineering", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 30,
             "desc": "SRE practices, SLOs, error budgets.", "why": "Engineering approach to operations.",
             "aliases": ["SRE"], "prereqs": ["Monitoring & Observability"]},
            {"name": "Communication", "level": "fundamental", "category": "soft_skill", "priority": "must_have", "hours": 10,
             "desc": "Cross-team collaboration.", "why": "DevOps bridges dev and ops teams."},
            {"name": "AWS Solutions Architect", "level": "advanced", "category": "certification", "priority": "optional", "hours": 40,
             "desc": "AWS Solutions Architect certification.", "why": "Validates cloud architecture skills.",
             "prereqs": ["Cloud Platforms"]},
        ],
    },
    {
        "title": "Cybersecurity Analyst",
        "slug": "cybersecurity-analyst",
        "description": "Protect organizations from cyber threats through risk assessment, security monitoring, incident response, and vulnerability management.",
        "icon": "shield",
        "color": "#ef4444",
        "skills": [
            {"name": "Networking Fundamentals", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 35,
             "desc": "TCP/IP, DNS, firewalls, VPNs, protocols.", "why": "All cybersecurity starts with understanding network communication."},
            {"name": "Linux", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 35,
             "desc": "Linux administration and command line.", "why": "Most security tools run on Linux."},
            {"name": "Operating Systems", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Windows, Linux, macOS internals.", "why": "Understanding how OSes work is critical for vulnerability analysis."},
            {"name": "Python", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Scripting for security automation.", "why": "Used for writing security tools and automating tasks."},
            {"name": "Security Fundamentals", "level": "fundamental", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "CIA triad, security frameworks, risk management.", "why": "Core principles that guide all security decisions.",
             "prereqs": ["Networking Fundamentals"]},
            {"name": "Cryptography", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Encryption, hashing, PKI, TLS.", "why": "Foundation of secure communications.",
             "prereqs": ["Security Fundamentals"]},
            {"name": "Network Security", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Firewalls, IDS/IPS, VPNs, network monitoring.", "why": "Protecting network perimeters from attack.",
             "prereqs": ["Networking Fundamentals", "Security Fundamentals"]},
            {"name": "Vulnerability Assessment", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Scanning, enumeration, vulnerability identification.", "why": "Finding weaknesses before attackers do.",
             "prereqs": ["Network Security"]},
            {"name": "SIEM", "level": "intermediate", "category": "tool", "priority": "must_have", "hours": 25,
             "desc": "Splunk, ELK, Azure Sentinel for log analysis.", "why": "Central tool for security monitoring and alerting.",
             "prereqs": ["Security Fundamentals"]},
            {"name": "Incident Response", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 25,
             "desc": "Detection, containment, eradication, recovery.", "why": "Structured approach to handling security breaches.",
             "prereqs": ["SIEM", "Network Security"]},
            {"name": "Web Application Security", "level": "intermediate", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "OWASP Top 10, XSS, SQLi, CSRF.", "why": "Web apps are the most common attack surface.",
             "prereqs": ["Security Fundamentals", "Python"]},
            {"name": "Penetration Testing", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 40,
             "desc": "Ethical hacking, Metasploit, Burp Suite.", "why": "Simulating attacks to find real vulnerabilities.",
             "prereqs": ["Vulnerability Assessment", "Web Application Security"]},
            {"name": "Cloud Security", "level": "advanced", "category": "technical", "priority": "must_have", "hours": 30,
             "desc": "Securing AWS, Azure, GCP environments.", "why": "Organizations are moving to the cloud rapidly.",
             "prereqs": ["Security Fundamentals"]},
            {"name": "Digital Forensics", "level": "advanced", "category": "technical", "priority": "recommended", "hours": 25,
             "desc": "Evidence collection, disk/memory analysis.", "why": "Investigating breaches and building legal cases.",
             "prereqs": ["Incident Response"]},
            {"name": "Compliance", "level": "intermediate", "category": "domain", "priority": "must_have", "hours": 20,
             "desc": "GDPR, HIPAA, SOC2, ISO 27001.", "why": "Security must align with regulatory requirements.",
             "prereqs": ["Security Fundamentals"]},
            {"name": "Git", "level": "fundamental", "category": "tool", "priority": "recommended", "hours": 10,
             "desc": "Version control for scripts and configs.", "why": "Track changes to security configurations."},
            {"name": "Analytical Thinking", "level": "fundamental", "category": "soft_skill", "priority": "must_have", "hours": 10,
             "desc": "Systematic approach to threat analysis.", "why": "Security analysts must think like attackers."},
            {"name": "CompTIA Security+", "level": "intermediate", "category": "certification", "priority": "recommended", "hours": 40,
             "desc": "Industry-standard entry cybersecurity cert.", "why": "Validates foundational security knowledge.",
             "prereqs": ["Security Fundamentals"]},
        ],
    },
]


def seed_database():
    init_db()
    db = SessionLocal()

    # Skip if already seeded
    if db.query(CareerPath).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    try:
        for career_data in CAREERS:
            career = CareerPath(
                title=career_data["title"],
                slug=career_data["slug"],
                description=career_data["description"],
                icon=career_data["icon"],
                color=career_data["color"],
            )
            db.add(career)
            db.flush()

            skill_objects = {}
            total_hours = 0

            # First pass: create all skills
            for i, s in enumerate(career_data["skills"]):
                slug = slugify(s["name"])
                skill = Skill(
                    career_path_id=career.id,
                    name=s["name"],
                    slug=slug,
                    description=s["desc"],
                    why_important=s.get("why", ""),
                    level=s["level"],
                    category=s["category"],
                    priority=s["priority"],
                    estimated_hours=s["hours"],
                )
                db.add(skill)
                db.flush()
                skill_objects[s["name"]] = skill
                total_hours += s["hours"]

                # Aliases
                for alias in s.get("aliases", []):
                    db.add(SkillAlias(skill_id=skill.id, alias=alias))

                # Roadmap node – auto-layout in a grid-like pattern
                layer = {"fundamental": 0, "intermediate": 1, "advanced": 2, "optional": 3}.get(s["level"], 0)
                level_index = sum(1 for sk in career_data["skills"][:i] if sk["level"] == s["level"])
                node = RoadmapNode(
                    career_path_id=career.id,
                    skill_id=skill.id,
                    position_x=level_index * 220 + 100,
                    position_y=layer * 200 + 100,
                    layer=layer,
                )
                db.add(node)

            # Second pass: create edges
            for s in career_data["skills"]:
                if "prereqs" in s:
                    target = skill_objects.get(s["name"])
                    for prereq_name in s["prereqs"]:
                        source = skill_objects.get(prereq_name)
                        if source and target:
                            db.add(RoadmapEdge(
                                career_path_id=career.id,
                                source_skill_id=source.id,
                                target_skill_id=target.id,
                            ))

            career.estimated_hours = total_hours
            db.flush()

            print(f"  ✓ {career.title}: {len(skill_objects)} skills, {total_hours}h estimated")

        db.commit()
        print("\n✅ Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
