"""Cybersecurity Analyst career seed data."""

CAREER = {
    "slug": "cybersecurity-analyst",
    "title": "Cybersecurity Analyst",
    "description": (
        "Defend organizations from attackers: monitor threats, hunt intrusions, "
        "harden systems and lead incident response across cloud and on-prem estates."
    ),
    "icon": "shield",
    "color": "#ef4444",
    "difficulty": "intermediate",
    "typical_roles": ["SOC Analyst", "Security Analyst", "Threat Hunter", "Incident Responder", "Penetration Tester"],
    "major_technologies": ["SIEM (Splunk)", "Wireshark", "Linux", "Python", "OWASP", "Burp Suite", "Nmap"],
}

SKILLS = [
    {
        "key": "networking", "name": "Networking Fundamentals", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 35,
        "description": "TCP/IP, OSI model, DNS, DHCP, routing, packet analysis with Wireshark.",
        "why_important": "Attacks traverse networks; you can't defend what you can't read.",
        "aliases": ["computer networks", "tcp/ip", "packet analysis"],
        "resources": [
            {"title": "Networking Basics", "platform": "Cisco Networking Academy", "url": "https://www.netacad.com/courses/networking-basics", "type": "course", "free": True, "difficulty": "beginner", "hours": 30},
            {"title": "Practical Packet Analysis (book)", "platform": "Book — No Starch Press", "url": "", "type": "book", "free": False, "difficulty": "intermediate", "hours": 15},
        ],
    },
    {
        "key": "linux", "name": "Linux Fundamentals", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 25,
        "description": "Command line, file permissions, logs, services — both as admin and as attacker target.",
        "why_important": "Servers, security tools and attackers all live on Linux.",
        "aliases": ["linux administration", "bash", "unix"],
        "resources": [
            {"title": "Linux Journey", "platform": "linuxjourney.com", "url": "https://linuxjourney.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 12},
            {"title": "Pre Security Path", "platform": "TryHackMe", "url": "https://tryhackme.com/path/outline/presecurity", "type": "practice", "free": True, "difficulty": "beginner", "hours": 40},
        ],
    },
    {
        "key": "security-fundamentals", "name": "Security Fundamentals", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 30,
        "description": "CIA triad, threat modeling, attack surfaces, defense-in-depth, security policies.",
        "why_important": "Shared vocabulary and mental models for every security conversation.",
        "aliases": ["information security", "infosec", "cyber security basics", "cybersecurity fundamentals"],
        "resources": [
            {"title": "Cybersecurity Fundamentals", "platform": "IBM SkillsBuild", "url": "https://skillsbuild.org/students/course-catalog/cybersecurity", "type": "course", "free": True, "difficulty": "beginner", "hours": 20},
            {"title": "Introduction to Cybersecurity", "platform": "Cisco Networking Academy", "url": "https://www.netacad.com/courses/introduction-to-cybersecurity", "type": "course", "free": True, "difficulty": "beginner", "hours": 15},
        ],
    },
    {
        "key": "python-scripting", "name": "Python for Security", "category": "technical", "level": "intermediate",
        "priority": "recommended", "hours": 30,
        "description": "Automating recon, parsing logs, writing scanners and exploit PoCs.",
        "why_important": "Security automation multiplies analyst effectiveness.",
        "aliases": ["python", "security scripting"],
        "resources": [
            {"title": "Automate the Boring Stuff with Python", "platform": "Book (free online)", "url": "https://automatetheboringstuff.com/", "type": "book", "free": True, "difficulty": "beginner", "hours": 20},
            {"title": "Violent Python examples", "platform": "GitHub", "url": "https://github.com/topics/security-tools", "type": "github", "free": True, "difficulty": "intermediate", "hours": 12},
        ],
    },
    {
        "key": "cryptography", "name": "Cryptography", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 25,
        "description": "Symmetric/asymmetric encryption, hashing, PKI/TLS, key management and common failures.",
        "why_important": "Encryption misconfigurations cause real breaches; interviews test concepts.",
        "aliases": ["encryption", "applied cryptography", "pki"],
        "resources": [
            {"title": "CryptoHack Challenges", "platform": "cryptohack.org", "url": "https://cryptohack.org/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 30},
            {"title": "Crypto 101 (free book)", "platform": "crypto101.io", "url": "https://www.crypto101.io/", "type": "book", "free": True, "difficulty": "beginner", "hours": 15},
        ],
    },
    {
        "key": "owasp-top-10", "name": "OWASP Top 10", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 15,
        "description": "Injection, broken access control, XSS and friends — the canonical web vulnerability list.",
        "why_important": "Baseline literacy for any role touching applications.",
        "aliases": ["owasp", "web vulnerabilities"],
        "resources": [
            {"title": "OWASP Top Ten Project", "platform": "OWASP", "url": "https://owasp.org/www-project-top-ten/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "web-app-security", "name": "Web Application Security", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 40,
        "description": "Hands-on exploitation and defense: SQLi, XSS, SSRF, auth bypass, session flaws.",
        "why_important": "Web apps are the #1 attack surface; practical skill beats theory.",
        "aliases": ["application security", "appsec"],
        "resources": [
            {"title": "Web Security Academy", "platform": "PortSwigger", "url": "https://portswigger.net/web-security", "type": "tutorial", "free": True, "difficulty": "intermediate", "hours": 60},
            {"title": "OWASP Juice Shop", "platform": "OWASP", "url": "https://owasp.org/www-project-juice-shop/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 15},
        ],
    },
    {
        "key": "penetration-testing", "name": "Penetration Testing", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 60,
        "description": "Methodical offensive testing: scoping, recon, enumeration, exploitation, reporting.",
        "why_important": "Red-team skills make blue-team analysts dramatically better.",
        "aliases": ["pentesting", "ethical hacking", "pen testing", "offensive security"],
        "resources": [
            {"title": "Junior Penetration Tester Path", "platform": "TryHackMe", "url": "https://tryhackme.com/path/outline/jrpenetrationtester", "type": "practice", "free": False, "difficulty": "intermediate", "hours": 100},
            {"title": "Hack The Box Academy", "platform": "HTB Academy", "url": "https://academy.hackthebox.com/", "type": "course", "free": True, "difficulty": "intermediate", "hours": 50},
        ],
    },
    {
        "key": "vulnerability-assessment", "name": "Vulnerability Assessment", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 22,
        "description": "Scanning with Nessus/OpenVAS/Nmap, CVSS scoring, remediation tracking.",
        "why_important": "Continuous vuln management is a core SOC deliverable.",
        "aliases": ["vulnerability scanning", "nmap", "nessus"],
        "resources": [
            {"title": "Nmap Reference Guide", "platform": "Official Docs", "url": "https://nmap.org/book/man.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "siem", "name": "SIEM & Log Analysis", "category": "tool", "level": "intermediate",
        "priority": "must_have", "hours": 35,
        "description": "Splunk/Sentinel queries, correlation rules, alert triage and log pipelines.",
        "why_important": "The SIEM console is home base for SOC analysts.",
        "aliases": ["splunk", "security information and event management", "microsoft sentinel"],
        "resources": [
            {"title": "Splunk Free Training", "platform": "Splunk", "url": "https://www.splunk.com/en_us/training/free-courses/overview.html", "type": "course", "free": True, "difficulty": "beginner", "hours": 15},
            {"title": "SOC Analyst Path", "platform": "TryHackMe", "url": "https://tryhackme.com/path/outline/soclevel1", "type": "practice", "free": False, "difficulty": "beginner", "hours": 60},
        ],
    },
    {
        "key": "incident-response", "name": "Incident Response", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 30,
        "description": "NIST lifecycle: preparation, detection, containment, eradication, recovery, lessons learned.",
        "why_important": "When breaches happen, structured response limits damage.",
        "aliases": ["soc operations", "ir lifecycle"],
        "resources": [
            {"title": "Incident Handler's Handbook", "platform": "SANS", "url": "https://www.sans.org/white-papers/33901/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 3},
        ],
    },
    {
        "key": "digital-forensics", "name": "Digital Forensics", "category": "technical", "level": "advanced",
        "priority": "optional", "hours": 35,
        "description": "Disk/memory acquisition, timeline analysis, chain of custody and forensic tooling.",
        "why_important": "Understanding 'what happened' requires evidence discipline.",
        "aliases": ["dfir", "forensics"],
        "resources": [
            {"title": "Digital Forensics Course", "platform": "CFReDS / NIST resources", "url": "https://cfreds.nist.gov/", "type": "practice", "free": True, "difficulty": "advanced", "hours": 20},
        ],
    },
    {
        "key": "threat-intelligence", "name": "Threat Intelligence", "category": "domain", "level": "advanced",
        "priority": "optional", "hours": 25,
        "description": "MITRE ATT&CK mapping, IOC management, threat feeds and proactive hunting hypotheses.",
        "why_important": "Mature SOCs hunt proactively instead of waiting for alerts.",
        "aliases": ["mitre att&ck", "threat hunting", "cyber threat intelligence"],
        "resources": [
            {"title": "MITRE ATT&CK Framework", "platform": "MITRE", "url": "https://attack.mitre.org/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "iam", "name": "Identity & Access Management", "category": "technical", "level": "intermediate",
        "priority": "recommended", "hours": 20,
        "description": "Authentication protocols, SSO/MFA, least privilege, Active Directory security.",
        "why_important": "Identity is the new perimeter; AD attacks dominate enterprise breaches.",
        "aliases": ["iam", "active directory", "access management", "sso", "mfa"],
        "resources": [
            {"title": "Zero to Hero: Active Directory Security", "platform": "TryHackMe rooms", "url": "https://tryhackme.com/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 10},
        ],
    },
    {
        "key": "cloud-security", "name": "Cloud Security", "category": "technical", "level": "advanced",
        "priority": "recommended", "hours": 30,
        "description": "Shared responsibility model, CSPM, IAM policies in AWS/Azure, container security.",
        "why_important": "Workloads have moved to cloud; so have the attacks.",
        "aliases": ["aws security", "azure security", "cloud security posture"],
        "resources": [
            {"title": "AWS Security Learning", "platform": "AWS Skill Builder", "url": "https://aws.amazon.com/training/", "type": "course", "free": True, "difficulty": "intermediate", "hours": 15},
        ],
    },
    {
        "key": "grc", "name": "Governance, Risk & Compliance", "category": "domain", "level": "intermediate",
        "priority": "optional", "hours": 22,
        "description": "ISO 27001, NIST CSF, GDPR/DPDP basics, risk registers and audit readiness.",
        "why_important": "Regulated industries hire GRC-aware analysts at premium rates.",
        "aliases": ["risk management", "compliance", "iso 27001", "nist csf"],
        "resources": [
            {"title": "NIST Cybersecurity Framework", "platform": "NIST", "url": "https://www.nist.gov/cyberframework", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "communication", "name": "Communication", 	"category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 8,
        "description": "Writing incident reports executives act on; briefing non-technical stakeholders calmly.",
        "why_important": "Security value is realized through influence, not just alerts.",
        "aliases": ["communication skills", "report writing"],
        "resources": [
            {"title": "Google Technical Writing Courses", "platform": "Google", "url": "https://developers.google.com/tech-writing", "type": "course", "free": True, "difficulty": "beginner", "hours": 3},
        ],
    },
    {
        "key": "problem-solving", "name": "Analytical Problem Solving", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 0,
        "description": "Triaging ambiguous alerts, correlating weak signals and reasoning about attacker intent.",
        "why_important": "Analysts face adversarial puzzles daily under time pressure.",
        "aliases": ["analytical thinking", "critical thinking"],
        "resources": [
            {"title": "CTF 101", "platform": "ctf101.org", "url": "https://ctf101.org/", "type": "practice", "free": True, "difficulty": "beginner", "hours": 8},
            {"title": "picoCTF", "platform": "CMU picoCTF", "url": "https://picoctf.org/", "type": "practice", "free": True, "difficulty": "beginner", "hours": 30},
        ],
    },
    {
        "key": "cert-comptia-security", "name": "CompTIA Security+", "category": "certification", "level": "optional",
        "priority": "recommended", "hours": 50,
        "description": "The standard entry-level security certification covering all baseline domains.",
        "why_important": "Most-cited requirement for junior security roles worldwide.",
        "aliases": ["security plus", "security+"],
        "resources": [
            {"title": "CompTIA Security+ Certification", "platform": "CompTIA", "url": "https://www.comptia.org/certifications/security", "type": "certification", "free": False, "difficulty": "beginner", "hours": 50},
        ],
    },
    {
        "key": "cert-ceh", "name": "Certified Ethical Hacker (CEH)", "category": "certification", "level": "optional",
        "priority": "optional", "hours": 60,
        "description": "Vendor certification validating offensive techniques and tooling breadth.",
        "why_important": "Common HR filter for offensive-security and SOC hybrid roles in India.",
        "aliases": ["ceh"],
        "resources": [
            {"title": "Certified Ethical Hacker Program", "platform": "EC-Council", "url": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/", "type": "certification", "free": False, "difficulty": "intermediate", "hours": 60},
        ],
    },
]

EDGES = [
    ("networking", "security-fundamentals"), ("networking", "vulnerability-assessment"),
    ("linux", "security-fundamentals"),
    ("security-fundamentals", "cryptography"), ("security-fundamentals", "owasp-top-10"),
    ("security-fundamentals", "iam"), ("security-fundamentals", "grc"),
    ("owasp-top-10", "web-app-security"), ("web-app-security", "penetration-testing"),
    ("linux", "penetration-testing"),
    ("networking", "siem"), ("siem", "incident-response"),
    ("incident-response", "digital-forensics"), ("digital-forensics", "threat-intelligence"),
    ("cloud-security", "iam"), ("python-scripting", "siem"),
    ("python-scripting", "penetration-testing"),
    ("cert-comptia-security", "security-fundamentals"),
    ("penetration-testing", "cert-ceh"),
]
