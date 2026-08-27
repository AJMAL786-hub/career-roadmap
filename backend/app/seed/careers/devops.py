"""DevOps Engineer career seed data."""

CAREER = {
    "slug": "devops-engineer",
    "title": "DevOps Engineer",
    "description": (
        "Own the path from commit to production: infrastructure as code, containers, "
        "CI/CD automation and reliable, observable cloud systems."
    ),
    "icon": "infinity",
    "color": "#f59e0b",
    "difficulty": "intermediate",
    "typical_roles": ["DevOps Engineer", "Platform Engineer", "SRE", "Cloud Engineer", "Infrastructure Engineer"],
    "major_technologies": ["Kubernetes", "Terraform", "AWS", "Docker", "CI/CD", "Prometheus", "Linux"],
}

SKILLS = [
    {
        "key": "linux", "name": "Linux Administration", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 35,
        "description": "Users/permissions, systemd services, processes, filesystems, SSH hardening, bash scripting.",
        "why_important": "Over 90% of servers run Linux; it's the substrate of all DevOps work.",
        "aliases": ["linux administration", "unix", "bash", "shell scripting"],
        "resources": [
            {"title": "Linux Journey", "platform": "linuxjourney.com", "url": "https://linuxjourney.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 12},
            {"title": "The Linux Command Line (book)", "platform": "Official", "url": "http://linuxcommand.org/tlcl.php", "type": "book", "free": True, "difficulty": "beginner", "hours": 25},
        ],
    },
    {
        "key": "networking", "name": "Networking Fundamentals", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 30,
        "description": "TCP/IP, DNS, HTTP/TLS, load balancing, firewalls, VPC/subnet design.",
        "why_important": "Most production outages trace back to DNS, networking or certificates.",
        "aliases": ["computer networks", "tcp/ip", "dns"],
        "resources": [
            {"title": "Computer Networking Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/@freecodecamp", "type": "video", "free": True, "difficulty": "beginner", "hours": 8},
        ],
    },
    {
        "key": "git", "name": "Git & GitHub", "category": "tool", "level": "fundamental",
        "priority": "must_have", "hours": 10,
        "description": "Branching workflows, PR review culture, monorepo vs multi-repo tradeoffs.",
        "why_important": "Everything in DevOps is versioned; GitOps extends Git to infrastructure.",
        "aliases": ["github", "version control"],
        "resources": [
            {"title": "Pro Git (official book)", "platform": "git-scm.com", "url": "https://git-scm.com/book/en/v2", "type": "book", "free": True, "difficulty": "beginner", "hours": 12},
        ],
    },
    {
        "key": "python-scripting", "name": "Python for Automation", "category": "technical", "level": "intermediate",
        "priority": "recommended", "hours": 30,
        "description": "Scripting APIs, parsing logs, boto3 automation and building internal tooling.",
        "why_important": "Glue-code automation is the daily bread of platform teams.",
        "aliases": ["python", "python scripting", "boto3"],
        "resources": [
            {"title": "Automate the Boring Stuff with Python", "platform": "Book (free online)", "url": "https://automatetheboringstuff.com/", "type": "book", "free": True, "difficulty": "beginner", "hours": 20},
        ],
    },
    {
        "key": "docker", "name": "Docker", "category": "tool", "level": "fundamental",
        "priority": "must_have", "hours": 22,
        "description": "Images/layers, Dockerfiles, compose, registries, multi-stage builds, rootless containers.",
        "why_important": "Containers are the packaging unit of modern deployment.",
        "aliases": ["containerization", "containers"],
        "resources": [
            {"title": "Docker Get Started", "platform": "Official Docs", "url": "https://docs.docker.com/get-started/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "kubernetes", "name": "Kubernetes", "category": "tool", "level": "advanced",
        "priority": "must_have", "hours": 50,
        "description": "Pods, Deployments, Services, Ingress, ConfigMaps/Secrets, RBAC, autoscaling, Helm.",
        "why_important": "The orchestration standard; the single most requested DevOps skill.",
        "aliases": ["k8s", "kubernetes orchestration", "helm"],
        "resources": [
            {"title": "Kubernetes Tutorials", "platform": "Official Docs", "url": "https://kubernetes.io/docs/tutorials/", "type": "docs", "free": True, "difficulty": "advanced", "hours": 12},
            {"title": "Interactive K8s Labs", "platform": "Killercoda", "url": "https://killercoda.com/kubernetes", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "terraform", "name": "Terraform (IaC)", "category": "tool", "level": "intermediate",
        "priority": "must_have", "hours": 30,
        "description": "HCL, providers, state management, modules, workspaces and drift detection.",
        "why_important": "Infrastructure-as-code is how modern teams provision anything.",
        "aliases": ["infrastructure as code", "iac", "opentofu"],
        "resources": [
            {"title": "Terraform Tutorials", "platform": "HashiCorp Developer", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "tutorial", "free": True, "difficulty": "intermediate", "hours": 15},
        ],
    },
    {
        "key": "ansible", "name": "Ansible", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 20,
        "description": "Playbooks, roles, idempotent configuration management across fleets.",
        "why_important": "Config management remains essential in VM-heavy enterprises.",
        "aliases": ["configuration management"],
        "resources": [
            {"title": "Ansible Getting Started", "platform": "Official Docs", "url": "https://docs.ansible.com/ansible/latest/getting_started/index.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "ci-cd", "name": "CI/CD Pipelines", "category": "tool", "level": "fundamental",
        "priority": "must_have", "hours": 25,
        "description": "Pipeline design, artifact promotion, environment strategy and deployment patterns (blue/green, canary).",
        "why_important": "The 'CD' is the heart of the job title.",
        "aliases": ["cicd", "ci cd", "continuous integration", "continuous delivery", "github actions", "gitlab ci"],
        "resources": [
            {"title": "GitHub Actions Documentation", "platform": "GitHub Docs", "url": "https://docs.github.com/en/actions", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "jenkins", "name": "Jenkins", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 18,
        "description": "Declarative pipelines, shared libraries and maintaining legacy CI estates.",
        "why_important": "Still entrenched in large enterprises; frequent JD mention.",
        "aliases": [],
        "resources": [
            {"title": "Jenkins Pipeline Getting Started", "platform": "Official Docs", "url": "https://www.jenkins.io/doc/pipeline/tour/getting-started/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 5},
        ],
    },
    {
        "key": "aws", "name": "AWS", "category": "tool", "level": "intermediate",
        "priority": "must_have", "hours": 45,
        "description": "EC2, VPC, S3, IAM, RDS, EKS, CloudWatch — core services for running production.",
        "why_important": "Largest cloud provider; most DevOps job descriptions assume AWS.",
        "aliases": ["amazon web services", "aws cloud", "ec2", "s3", "eks"],
        "resources": [
            {"title": "AWS Training and Certification", "platform": "AWS Skill Builder", "url": "https://aws.amazon.com/training/", "type": "course", "free": True, "difficulty": "beginner", "hours": 20},
        ],
    },
    {
        "key": "azure", "name": "Microsoft Azure", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 30,
        "description": "Azure VMs, AKS, DevOps services and hybrid enterprise environments.",
        "why_important": "Strong enterprise presence, especially in regulated industries.",
        "aliases": ["microsoft azure"],
        "resources": [
            {"title": "Azure Fundamentals Learning Path", "platform": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/azure/", "type": "course", "free": True, "difficulty": "beginner", "hours": 12},
        ],
    },
    {
        "key": "google-cloud", "name": "Google Cloud Platform", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 28,
        "description": "Compute Engine, GKE, Cloud Run and Google-native managed services.",
        "why_important": "GKE is widely considered best-in-class managed Kubernetes.",
        "aliases": ["gcp", "google cloud platform"],
        "resources": [
            {"title": "Google Cloud Skills Boost", "platform": "Google Cloud", "url": "https://www.cloudskillsboost.google/", "type": "course", "free": True, "difficulty": "beginner", "hours": 15},
        ],
    },
    {
        "key": "monitoring-observability", "name": "Monitoring & Observability", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 30,
        "description": "Metrics/logs/traces, Prometheus, Grafana dashboards, alert design and SLOs.",
        "why_important": "You can't operate what you can't observe; SLOs drive reliability decisions.",
        "aliases": ["observability", "prometheus", "grafana", "datadog"],
        "resources": [
            {"title": "Prometheus Introduction", "platform": "Official Docs", "url": "https://prometheus.io/docs/introduction/overview/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 4},
            {"title": "Grafana Tutorials", "platform": "Grafana Labs", "url": "https://grafana.com/tutorials/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "sre-practices", "name": "Site Reliability Engineering", "category": "domain", "level": "advanced",
        "priority": "recommended", "hours": 25,
        "description": "Error budgets, incident command, postmortems, capacity planning and toil reduction.",
        "why_important": "SRE practices define how top engineering orgs run production.",
        "aliases": ["sre", "site reliability engineering", "incident management"],
        "resources": [
            {"title": "The SRE Book (free online)", "platform": "Google", "url": "https://sre.google/books/", "type": "book", "free": True, "difficulty": "advanced", "hours": 30},
        ],
    },
    {
        "key": "cloud-security", "name": "Cloud Security Basics", "category": "technical", "level": "intermediate",
        "priority": "recommended", "hours": 20,
        "description": "IAM least privilege, secrets management, network policies and security groups.",
        "why_important": "Misconfigured cloud permissions are the #1 breach vector.",
        "aliases": ["secrets management", "vault"],
        "resources": [
            {"title": "AWS Security Fundamentals", "platform": "AWS Skill Builder", "url": "https://aws.amazon.com/training/", "type": "course", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "gitops", "name": "GitOps", "category": "technical", "level": "advanced",
        "priority": "optional", "hours": 15,
        "description": "Declarative delivery with Argo CD/Flux where Git state equals cluster state.",
        "why_important": "Fast-growing pattern for Kubernetes-native deployment.",
        "aliases": ["argocd", "argo cd", "flux"],
        "resources": [
            {"title": "Argo CD Documentation", "platform": "Argo Project", "url": "https://argo-cd.readthedocs.io/en/stable/", "type": "docs", "free": True, "difficulty": "advanced", "hours": 6},
        ],
    },
    {
        "key": "service-mesh", "name": "Service Mesh", "category": "technical", "level": "advanced",
        "priority": "optional", "hours": 18,
        "description": "Istio/Linkerd sidecars, mTLS between services, traffic splitting and mesh observability.",
        "why_important": "Large microservice estates adopt meshes for zero-trust traffic.",
        "aliases": ["istio", "linkerd"],
        "resources": [
            {"title": "Istio Documentation", "platform": "Istio", "url": "https://istio.io/latest/docs/", "type": "docs", "free": True, "difficulty": "advanced", "hours": 8},
        ],
    },
    {
        "key": "communication", "name": "Communication & Documentation", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 10,
        "description": "Runbooks, postmortem writing, on-call handoffs and cross-team coordination.",
        "why_important": "During incidents, clear communication matters more than fast typing.",
        "aliases": ["technical writing", "documentation"],
        "resources": [
            {"title": "Google Technical Writing Courses", "platform": "Google", "url": "https://developers.google.com/tech-writing", "type": "course", "free": True, "difficulty": "beginner", "hours": 3},
        ],
    },
    {
        "key": "problem-solving", "name": "Problem Solving", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 0,
        "description": "Systematic debugging under pressure: isolate variables, form hypotheses, verify.",
        "why_important": "Production incidents reward calm structured thinking.",
        "aliases": ["analytical thinking", "troubleshooting"],
        "resources": [
            {"title": "The SRE Workbook (free online)", "platform": "Google", "url": "https://sre.google/workbook/incident-response/", "type": "book", "free": True, "difficulty": "intermediate", "hours": 10},
        ],
    },
    {
        "key": "cert-cka", "name": "Certified Kubernetes Administrator (CKA)", "category": "certification", "level": "optional",
        "priority": "recommended", "hours": 60,
        "description": "Hands-on performance-based exam validating real Kubernetes admin skills.",
        "why_important": "The most respected hands-on DevOps certification.",
        "aliases": ["cka", "ckad"],
        "resources": [
            {"title": "CKA Certification", "platform": "CNCF", "url": "https://www.cncf.io/training/certification/cka/", "type": "certification", "free": False, "difficulty": "advanced", "hours": 60},
        ],
    },
    {
        "key": "cert-aws-saa", "name": "AWS Solutions Architect – Associate", "category": "certification", "level": "optional",
        "priority": "recommended", "hours": 55,
        "description": "Validates designing resilient, cost-optimized architectures on AWS.",
        "why_important": "Highest-volume cloud certification requested by recruiters.",
        "aliases": ["aws saa", "aws solutions architect"],
        "resources": [
            {"title": "AWS Solutions Architect Associate", "platform": "AWS", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "type": "certification", "free": True, "difficulty": "intermediate", "hours": 55},
        ],
    },
]

EDGES = [
    ("linux", "networking"), ("linux", "docker"), ("linux", "python-scripting"),
    ("git", "ci-cd"), ("docker", "kubernetes"),
    ("ci-cd", "jenkins"), ("ci-cd", "gitops"), ("kubernetes", "gitops"),
    ("aws", "terraform"), ("terraform", "ansible"),
    ("kubernetes", "service-mesh"), ("monitoring-observability", "sre-practices"),
    ("networking", "cloud-security"), ("cloud-security", "kubernetes"),
    ("aws", "azure"), ("aws", "google-cloud"),
    ("kubernetes", "cert-cka"), ("aws", "cert-aws-saa"),
    ("python-scripting", "monitoring-observability"),
]
