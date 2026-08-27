"""Full Stack Developer career seed data."""

CAREER = {
    "slug": "full-stack-developer",
    "title": "Full Stack Developer",
    "description": (
        "Build complete web products end-to-end: pixel-perfect frontends, robust "
        "APIs, databases, and cloud deployment — the most in-demand engineering role."
    ),
    "icon": "layers",
    "color": "#10b981",
    "difficulty": "beginner-friendly",
    "typical_roles": ["Full Stack Developer", "Frontend Engineer", "Backend Engineer", "Product Engineer", "Web Developer"],
    "major_technologies": ["React", "Node.js", "TypeScript", "PostgreSQL", "Next.js", "AWS", "Tailwind CSS"],
}

SKILLS = [
    {
        "key": "html", "name": "HTML", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 15,
        "description": "Semantic markup, forms, media and document structure — the skeleton of the web.",
        "why_important": "Everything renders into HTML; semantic markup powers SEO and accessibility.",
        "aliases": ["html5"],
        "resources": [
            {"title": "Learn HTML", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "docs", "free": True, "difficulty": "beginner", "hours": 8},
            {"title": "Responsive Web Design Certification", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "type": "course", "free": True, "difficulty": "beginner", "hours": 300},
        ],
    },
    {
        "key": "css", "name": "CSS", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 30,
        "description": "Flexbox, Grid, responsive design, transitions and modern layout techniques.",
        "why_important": "Layout fluency separates real frontend engineers from tutorial followers.",
        "aliases": ["css3", "modern css", "responsive design"],
        "resources": [
            {"title": "Learn CSS", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS", "type": "docs", "free": True, "difficulty": "beginner", "hours": 15},
            {"title": "Flexbox Froggy & Grid Garden", "platform": "Practice games", "url": "https://flexboxfroggy.com/", "type": "practice", "free": True, "difficulty": "beginner", "hours": 3},
        ],
    },
    {
        "key": "javascript", "name": "JavaScript", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 60,
        "description": "Closures, prototypes, async/await, event loop, DOM and ES6+ features.",
        "why_important": "The programming language of both browser and server (via Node).",
        "aliases": ["js", "es6", "vanilla javascript"],
        "resources": [
            {"title": "The Modern JavaScript Tutorial", "platform": "javascript.info", "url": "https://javascript.info/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 60},
            {"title": "JavaScript Algorithms and Data Structures", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "course", "free": True, "difficulty": "beginner", "hours": 300},
        ],
    },
    {
        "key": "git", "name": "Git & GitHub", "category": "tool", "level": "fundamental",
        "priority": "must_have", "hours": 10,
        "description": "Branching strategies, pull requests, code review and open-source contribution flow.",
        "why_important": "Every team runs on Git-based collaboration.",
        "aliases": ["github", "version control"],
        "resources": [
            {"title": "Pro Git (official book)", "platform": "git-scm.com", "url": "https://git-scm.com/book/en/v2", "type": "book", "free": True, "difficulty": "beginner", "hours": 12},
            {"title": "GitHub Skills", "platform": "GitHub", "url": "https://skills.github.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "typescript", "name": "TypeScript", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 25,
        "description": "Static types, generics, interfaces and safe refactoring at scale.",
        "why_important": "Default choice for new production codebases on both frontend and backend.",
        "aliases": ["ts"],
        "resources": [
            {"title": "TypeScript Handbook", "platform": "Official Docs", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 12},
            {"title": "TypeScript Course", "platform": "Total TypeScript (free tutorials)", "url": "https://www.totaltypescript.com/tutorials", "type": "tutorial", "free": True, "difficulty": "intermediate", "hours": 15},
        ],
    },
    {
        "key": "react", "name": "React", "category": "framework", "level": "intermediate",
        "priority": "must_have", "hours": 50,
        "description": "Components, hooks, state management, context, performance and React 18 patterns.",
        "why_important": "#1 frontend framework by job volume worldwide.",
        "aliases": ["react.js", "reactjs", "react js"],
        "resources": [
            {"title": "Learn React", "platform": "Official Docs (react.dev)", "url": "https://react.dev/learn", "type": "docs", "free": True, "difficulty": "beginner", "hours": 20},
            {"title": "React Course", "platform": "freeCodeCamp (YouTube)", "url": "https://www.youtube.com/@freecodecamp", "type": "video", "free": True, "difficulty": "beginner", "hours": 12},
        ],
    },
    {
        "key": "redux", "name": "State Management (Redux/Zustand)", "category": "framework", "level": "advanced",
        "priority": "optional", "hours": 20,
        "description": "Global state architecture, Redux Toolkit, Zustand stores and server-state caching.",
        "why_important": "Complex apps need predictable state; interviews probe it often.",
        "aliases": ["redux toolkit", "zustand", "state management"],
        "resources": [
            {"title": "Redux Essentials Tutorial", "platform": "Official Docs", "url": "https://redux.js.org/tutorials/essentials/part-1-overview-concepts", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 10},
        ],
    },
    {
        "key": "nextjs", "name": "Next.js", "category": "framework", "level": "advanced",
        "priority": "recommended", "hours": 30,
        "description": "App router, SSR/SSG/ISR, API routes and full-stack React deployment on Vercel.",
        "why_important": "Fastest-growing meta-framework; dominant for new React production apps.",
        "aliases": ["next.js", "nextjs"],
        "resources": [
            {"title": "Learn Next.js", "platform": "Official Course", "url": "https://nextjs.org/learn", "type": "course", "free": True, "difficulty": "intermediate", "hours": 16},
        ],
    },
    {
        "key": "tailwind-css", "name": "Tailwind CSS", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 12,
        "description": "Utility-first styling, design systems and responsive composition speed.",
        "why_important": "Has become the default styling approach in modern React teams.",
        "aliases": ["tailwind", "tailwindcss"],
        "resources": [
            {"title": "Tailwind CSS Documentation", "platform": "Official Docs", "url": "https://tailwindcss.com/docs/installation", "type": "docs", "free": True, "difficulty": "beginner", "hours": 4},
        ],
    },
    {
        "key": "nodejs", "name": "Node.js & Express", "category": "framework", "level": "intermediate",
        "priority": "must_have", "hours": 40,
        "description": "Event loop, streams, middleware, REST routing and npm ecosystem management.",
        "why_important": "JavaScript on the server completes the full stack story.",
        "aliases": ["node", "node.js", "express", "express.js"],
        "resources": [
            {"title": "Introduction to Node.js", "platform": "Official Learn Hub", "url": "https://nodejs.org/en/learn", "type": "docs", "free": True, "difficulty": "beginner", "hours": 10},
            {"title": "Express Guide", "platform": "Official Docs", "url": "https://expressjs.com/en/guide/routing.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "rest-apis", "name": "REST APIs", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 25,
        "description": "Resource modeling, HTTP semantics, status codes, pagination, auth and versioning.",
        "why_important": "APIs are the contract between frontend and backend; interviews drill them.",
        "aliases": ["restful api development", "rest api development", "restful apis", "api design", "api development"],
        "resources": [
            {"title": "RESTful Web API Design", "platform": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/modules/build-web-api-aspnet-core/", "type": "course", "free": True, "difficulty": "intermediate", "hours": 4},
        ],
    },
    {
        "key": "graphql", "name": "GraphQL", "category": "framework", "level": "advanced",
        "priority": "optional", "hours": 18,
        "description": "Schema design, queries/mutations, resolvers and when GraphQL beats REST.",
        "why_important": "Common at product companies with complex client data needs.",
        "aliases": [],
        "resources": [
            {"title": "GraphQL Learn", "platform": "Official Docs", "url": "https://graphql.org/learn/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 6},
        ],
    },
    {
        "key": "sql", "name": "SQL", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 25,
        "description": "Relational modeling, joins, indexes and transactions behind application data.",
        "why_important": "Nearly every app persists relational data; SQL screens are universal.",
        "aliases": ["structured query language"],
        "resources": [
            {"title": "SQLBolt Interactive Lessons", "platform": "SQLBolt", "url": "https://sqlbolt.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 8},
        ],
    },
    {
        "key": "postgresql", "name": "PostgreSQL", "category": "tool", "level": "intermediate",
        "priority": "must_have", "hours": 22,
        "description": "Schema migrations, indexing strategy, EXPLAIN plans and JSONB usage.",
        "why_important": "Most-loved production database; default choice for new products.",
        "aliases": ["postgres"],
        "resources": [
            {"title": "PostgreSQL Tutorial", "platform": "Official Docs", "url": "https://www.postgresql.org/docs/current/tutorial.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
            {"title": "PostgreSQL Exercises", "platform": "pgexercises.com", "url": "https://pgexercises.com/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "mongodb", "name": "MongoDB", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 16,
        "description": "Document modeling, aggregation pipeline and Mongoose ODM patterns.",
        "why_important": "Popular in MERN stacks and flexible-schema startups.",
        "aliases": ["mongo", "nosql"],
        "resources": [
            {"title": "MongoDB University Free Courses", "platform": "MongoDB", "url": "https://learn.mongodb.com/", "type": "course", "free": True, "difficulty": "beginner", "hours": 14},
        ],
    },
    {
        "key": "web-security", "name": "Web Security Fundamentals", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 18,
        "description": "OWASP Top 10, XSS/CSRF/SQLi prevention, JWT sessions, password hashing and HTTPS.",
        "why_important": "Shipping insecure auth or storage is a fireable class of bug.",
        "aliases": ["owasp top 10", "application security", "authentication & authorization"],
        "resources": [
            {"title": "OWASP Top Ten Project", "platform": "OWASP", "url": "https://owasp.org/www-project-top-ten/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 5},
            {"title": "Web Security Academy", "platform": "PortSwigger", "url": "https://portswigger.net/web-security", "type": "tutorial", "free": True, "difficulty": "intermediate", "hours": 30},
        ],
    },
    {
        "key": "testing", "name": "Testing (Jest/Vitest/Playwright)", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 22,
        "description": "Unit tests, integration tests, component testing and end-to-end browser automation.",
        "why_important": "Teams without tests ship regressions; CI gates depend on them.",
        "aliases": ["unit testing", "test automation", "jest", "vitest", "e2e testing"],
        "resources": [
            {"title": "Testing Library Documentation", "platform": "Testing Library", "url": "https://testing-library.com/docs/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "accessibility", "name": "Accessibility (a11y)", "category": "technical", "level": "intermediate",
        "priority": "recommended", "hours": 12,
        "description": "WCAG basics, ARIA roles, keyboard navigation and inclusive component design.",
        "why_important": "Legal requirements plus dramatically better UX; rising interview topic.",
        "aliases": ["a11y", "wcag"],
        "resources": [
            {"title": "Accessibility Overview", "platform": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/Accessibility", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "web-performance", "name": "Performance Optimization", "category": "technical", "level": "advanced",
        "priority": "recommended", "hours": 18,
        "description": "Core Web Vitals, code splitting, lazy loading, memoization and bundle analysis.",
        "why_important": "Speed directly moves conversion; senior interviews test optimization thinking.",
        "aliases": ["performance tuning", "core web vitals"],
        "resources": [
            {"title": "Web Vitals Guide", "platform": "web.dev (Google)", "url": "https://web.dev/articles/vitals", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 5},
        ],
    },
    {
        "key": "docker", "name": "Docker", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 18,
        "description": "Containerize apps for consistent local dev and production parity.",
        "why_important": "\"Works on my machine\" ends where containers begin.",
        "aliases": ["containerization"],
        "resources": [
            {"title": "Docker Get Started", "platform": "Official Docs", "url": "https://docs.docker.com/get-started/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "ci-cd", "name": "CI/CD Pipelines", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 16,
        "description": "Automated lint/test/build/deploy workflows with GitHub Actions or similar.",
        "why_important": "Deployment automation is expected of every product engineer now.",
        "aliases": ["cicd", "github actions", "continuous integration"],
        "resources": [
            {"title": "GitHub Actions Documentation", "platform": "GitHub Docs", "url": "https://docs.github.com/en/actions", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "aws", "name": "Cloud Deployment (AWS)", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 30,
        "description": "EC2/S3/RDS basics, environment config and shipping apps to production cloud infra.",
        "why_important": "Full stack means owning your deployment story.",
        "aliases": ["amazon web services", "cloud computing", "deployment"],
        "resources": [
            {"title": "AWS Get Started Guides", "platform": "Official Docs", "url": "https://aws.amazon.com/getting-started/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "system-design", "name": "System Design", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 40,
        "description": "Scaling, caching, load balancing, queues, CAP tradeoffs and designing under constraints.",
        "why_important": "The make-or-break interview round for mid/senior roles.",
        "aliases": ["distributed systems", "system architecture", "scalability"],
        "resources": [
            {"title": "System Design Primer", "platform": "GitHub", "url": "https://github.com/donnemartin/system-design-primer", "type": "github", "free": True, "difficulty": "advanced", "hours": 40},
        ],
    },
    {
        "key": "microservices", "name": "Microservices Architecture", "category": "technical", "level": "advanced",
        "priority": "optional", "hours": 28,
        "description": "Service boundaries, inter-service communication and distributed failure handling.",
        "why_important": "Large orgs decompose monoliths; understanding tradeoffs prevents cargo-culting.",
        "aliases": [],
        "resources": [
            {"title": "Microservices Patterns", "platform": "microservices.io", "url": "https://microservices.io/patterns/index.html", "type": "docs", "free": True, "difficulty": "advanced", "hours": 12},
        ],
    },
    {
        "key": "agile", "name": "Agile & Scrum", "category": "domain", "level": "fundamental",
        "priority": "recommended", "hours": 8,
        "description": "Sprints, standups, estimation, retros and working within product delivery cycles.",
        "why_important": "Virtually all product teams run some flavor of agile.",
        "aliases": ["agile methodologies", "scrum"],
        "resources": [
            {"title": "Agile with Atlassian Jira", "platform": "Coursera (audit free)", "url": "https://www.coursera.org/learn/agile-atlassian-jira", "type": "course", "free": False, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "communication", "name": "Communication", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 8,
        "description": "Writing clear PRs/docs, asking scoped questions and syncing with designers/PMs.",
        "why_important": "Cross-functional collaboration is the daily reality of product teams.",
        "aliases": ["communication skills"],
        "resources": [
            {"title": "Google Technical Writing Courses", "platform": "Google", "url": "https://developers.google.com/tech-writing", "type": "course", "free": True, "difficulty": "beginner", "hours": 3},
        ],
    },
    {
        "key": "problem-solving", "name": "Problem Solving & DSA", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 0,
        "description": "Arrays, hashmaps, trees, graphs and complexity analysis for coding screens.",
        "why_important": "DSA rounds remain the primary hiring filter at top companies.",
        "aliases": ["data structures and algorithms", "dsa", "leetcode"],
        "resources": [
            {"title": "NeetCode Roadmap", "platform": "neetcode.io", "url": "https://neetcode.io/roadmap", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 100},
            {"title": "Top Interview 150 Study Plan", "platform": "LeetCode", "url": "https://leetcode.com/studyplan/top-interview-150/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 80},
        ],
    },
    {
        "key": "cert-meta-frontend", "name": "Meta Front-End Developer Certificate", "category": "certification", "level": "optional",
        "priority": "optional", "hours": 60,
        "description": "Structured credential covering React, UI/UX principles and a capstone.",
        "why_important": "Useful signal for self-taught developers entering the market.",
        "aliases": [],
        "resources": [
            {"title": "Meta Front-End Developer Certificate", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer", "type": "certification", "free": False, "difficulty": "beginner", "hours": 210},
        ],
    },
]

EDGES = [
    ("html", "css"), ("css", "javascript"), ("javascript", "git"),
    ("javascript", "typescript"), ("javascript", "react"),
    ("react", "redux"), ("react", "nextjs"), ("css", "tailwind-css"),
    ("javascript", "nodejs"), ("nodejs", "rest-apis"),
    ("rest-apis", "graphql"), ("sql", "postgresql"),
    ("rest-apis", "mongodb"), ("rest-apis", "web-security"),
    ("javascript", "testing"), ("css", "accessibility"),
    ("react", "web-performance"), ("typescript", "web-performance"),
    ("docker", "ci-cd"), ("git", "ci-cd"), ("ci-cd", "aws"),
    ("rest-apis", "system-design"), ("postgresql", "system-design"),
    ("system-design", "microservices"), ("docker", "microservices"),
    ("typescript", "testing"),
]
