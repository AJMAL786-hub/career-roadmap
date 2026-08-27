"""Data Scientist career seed data."""

CAREER = {
    "slug": "data-scientist",
    "title": "Data Scientist",
    "description": (
        "Turn raw data into decisions: statistical analysis, experimentation, "
        "predictive modeling and executive storytelling that drives product strategy."
    ),
    "icon": "line-chart",
    "color": "#0ea5e9",
    "difficulty": "intermediate",
    "typical_roles": ["Data Scientist", "Product Analyst", "Decision Scientist", "Quantitative Analyst"],
    "major_technologies": ["Python", "SQL", "scikit-learn", "Tableau", "A/B Testing", "Statistics"],
}

SKILLS = [
    {
        "key": "python", "name": "Python", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 55,
        "description": "Core Python plus the scientific stack (NumPy/Pandas) for analysis and modeling.",
        "why_important": "The default language for analysis and ML across the industry.",
        "aliases": ["Python 3", "Python programming"],
        "resources": [
            {"title": "Official Python Tutorial", "platform": "Official Docs", "url": "https://docs.python.org/3/tutorial/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 15},
            {"title": "Data Analysis with Python", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "type": "course", "free": True, "difficulty": "beginner", "hours": 250},
        ],
    },
    {
        "key": "sql", "name": "SQL", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 35,
        "description": "Complex joins, CTEs, window functions — the #1 screened skill in DS interviews.",
        "why_important": "Data scientists spend more time querying warehouses than training models.",
        "aliases": ["structured query language", "advanced sql"],
        "resources": [
            {"title": "SQLBolt Interactive Lessons", "platform": "SQLBolt", "url": "https://sqlbolt.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 8},
            {"title": "Advanced SQL Tutorial", "platform": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "type": "tutorial", "free": True, "difficulty": "intermediate", "hours": 12},
            {"title": "SQL Exercises", "platform": "pgexercises.com", "url": "https://pgexercises.com/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "statistics", "name": "Statistics & Probability", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 55,
        "description": "Distributions, hypothesis tests, confidence intervals, regression and Bayesian thinking.",
        "why_important": "Statistics separates a data scientist from a dashboard builder.",
        "aliases": ["statistics & probability", "statistical inference"],
        "resources": [
            {"title": "Statistics and Probability", "platform": "Khan Academy", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "course", "free": True, "difficulty": "beginner", "hours": 40},
            {"title": "StatQuest with Josh Starmer", "platform": "YouTube", "url": "https://www.youtube.com/@statquest", "type": "video", "free": True, "difficulty": "beginner", "hours": 20},
        ],
    },
    {
        "key": "excel", "name": "Excel / Spreadsheets", "category": "tool", "level": "fundamental",
        "priority": "recommended", "hours": 15,
        "description": "Pivot tables, VLOOKUP/XLOOKUP, quick analyses stakeholders actually open.",
        "why_important": "Business teams live in spreadsheets; you will be asked to deliver in them.",
        "aliases": ["microsoft excel", "advanced excel", "spreadsheets"],
        "resources": [
            {"title": "Excel Skills for Business", "platform": "Coursera (audit free)", "url": "https://www.coursera.org/specializations/excel", "type": "course", "free": False, "difficulty": "beginner", "hours": 40},
        ],
    },
    {
        "key": "git", "name": "Git & Version Control", "category": "tool", "level": "fundamental",
        "priority": "must_have", "hours": 8,
        "description": "Track analysis code, share reproducible notebooks via GitHub.",
        "why_important": "Reproducibility of analysis is a baseline professional expectation.",
        "aliases": ["github", "version control"],
        "resources": [
            {"title": "Pro Git (official book)", "platform": "git-scm.com", "url": "https://git-scm.com/book/en/v2", "type": "book", "free": True, "difficulty": "beginner", "hours": 12},
        ],
    },
    {
        "key": "numpy", "name": "NumPy", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 20,
        "description": "Fast array math underlying pandas, scikit-learn and statsmodels.",
        "why_important": "Vectorized operations make analysis code clean and fast.",
        "aliases": [],
        "resources": [
            {"title": "NumPy: The Absolute Basics", "platform": "Official Docs", "url": "https://numpy.org/doc/stable/user/absolute_beginners.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "pandas", "name": "Pandas", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 32,
        "description": "Merging, reshaping, time series, missing-data handling on real messy datasets.",
        "why_important": "The workhorse of every data science workflow.",
        "aliases": [],
        "resources": [
            {"title": "Pandas Getting Started", "platform": "Official Docs", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 10},
            {"title": "Pandas Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/pandas", "type": "course", "free": True, "difficulty": "beginner", "hours": 4},
        ],
    },
    {
        "key": "eda", "name": "Exploratory Data Analysis", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 30,
        "description": "Systematic profiling: distributions, outliers, correlations, segmentation hypotheses.",
        "why_important": "EDA quality determines whether downstream models find signal or noise.",
        "aliases": ["exploratory data analysis", "data exploration"],
        "resources": [
            {"title": "Data Analysis Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/data-analysis", "type": "course", "free": True, "difficulty": "beginner", "hours": 4},
        ],
    },
    {
        "key": "matplotlib", "name": "Matplotlib & Seaborn", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 14,
        "description": "Publication-quality charts for distributions, relationships and model diagnostics.",
        "why_important": "Charts are how analysis persuades.",
        "aliases": ["seaborn"],
        "resources": [
            {"title": "Matplotlib Tutorials", "platform": "Official Docs", "url": "https://matplotlib.org/stable/tutorials/index.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
            {"title": "Data Visualization Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/data-visualization", "type": "course", "free": True, "difficulty": "beginner", "hours": 4},
        ],
    },
    {
        "key": "tableau", "name": "Tableau", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 25,
        "description": "Interactive dashboards, calculated fields and self-serve analytics for business users.",
        "why_important": "The most-requested BI tool in DS job postings.",
        "aliases": [],
        "resources": [
            {"title": "Tableau Training & Tutorials", "platform": "Tableau", "url": "https://www.tableau.com/learn/training", "type": "video", "free": True, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "power-bi", "name": "Power BI", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 20,
        "description": "DAX measures, data models and enterprise reporting on Microsoft stack.",
        "why_important": "Standard BI layer in enterprises running Azure/Microsoft 365.",
        "aliases": ["powerbi"],
        "resources": [
            {"title": "Power BI Training (Microsoft Learn)", "platform": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "type": "course", "free": True, "difficulty": "beginner", "hours": 12},
        ],
    },
    {
        "key": "machine-learning", "name": "Machine Learning", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 75,
        "description": "Regression, classification, clustering, ensembles and rigorous model evaluation.",
        "why_important": "Predictive modeling is the core value-add of the role.",
        "aliases": ["ml", "predictive modeling", "machine learning algorithms"],
        "resources": [
            {"title": "Machine Learning Specialization (Andrew Ng)", "platform": "Coursera (audit free)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "course", "free": False, "difficulty": "beginner", "hours": 90},
        ],
    },
    {
        "key": "scikit-learn", "name": "scikit-learn", "category": "framework", "level": "intermediate",
        "priority": "must_have", "hours": 30,
        "description": "Pipelines, cross-validation, hyperparameter search and metrics done right.",
        "why_important": "Industry-standard implementation of classical ML.",
        "aliases": ["sklearn"],
        "resources": [
            {"title": "scikit-learn Tutorials", "platform": "Official Docs", "url": "https://scikit-learn.org/stable/tutorial/index.html", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 8},
            {"title": "Intermediate ML Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intermediate-machine-learning", "type": "course", "free": True, "difficulty": "intermediate", "hours": 4},
        ],
    },
    {
        "key": "feature-engineering", "name": "Feature Engineering", "category": "technical", "level": "advanced",
        "priority": "recommended", "hours": 22,
        "description": "Encoding, interactions, leakage prevention and domain-informed variable creation.",
        "why_important": "Feature quality dominates model choice on tabular business problems.",
        "aliases": [],
        "resources": [
            {"title": "Feature Engineering Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/feature-engineering", "type": "course", "free": True, "difficulty": "intermediate", "hours": 5},
        ],
    },
    {
        "key": "a-b-testing", "name": "A/B Testing & Experimentation", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 30,
        "description": "Power analysis, randomization, sequential testing and reading experiment results honestly.",
        "why_important": "Product data science roles are won on experimentation expertise.",
        "aliases": ["ab testing", "experimentation", "split testing"],
        "resources": [
            {"title": "A/B Testing Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/ab-testing?utm_source=local", "type": "course", "free": True, "difficulty": "intermediate", "hours": 4},
            {"title": "Trustworthy Online Controlled Experiments", "platform": "Book — Cambridge Univ Press", "url": "", "type": "book", "free": False, "difficulty": "advanced", "hours": 25},
        ],
    },
    {
        "key": "time-series", "name": "Time Series Analysis", "category": "technical", "level": "advanced",
        "priority": "recommended", "hours": 25,
        "description": "Stationarity, ARIMA, Prophet-style decomposition and forecasting evaluation.",
        "why_important": "Forecasting revenue/demand is among the most common DS deliverables.",
        "aliases": ["forecasting", "time series forecasting"],
        "resources": [
            {"title": "Time Series Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/time-series", "type": "course", "free": True, "difficulty": "intermediate", "hours": 4},
        ],
    },
    {
        "key": "nlp-basics", "name": "NLP for Data Science", "category": "technical", "level": "advanced",
        "priority": "optional", "hours": 28,
        "description": "Text cleaning, TF-IDF, embeddings and transformer classifiers for text analytics.",
        "why_important": "Customer feedback/VOC analytics increasingly requires text modeling.",
        "aliases": ["text analytics", "natural language processing"],
        "resources": [
            {"title": "NLP Course", "platform": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "type": "course", "free": True, "difficulty": "intermediate", "hours": 25},
        ],
    },
    {
        "key": "spark", "name": "Apache Spark", "category": "tool", "level": "advanced",
        "priority": "optional", "hours": 32,
        "description": "PySpark for large-scale feature computation and distributed EDA.",
        "why_important": "Enterprises with big data platforms expect Spark literacy for senior DS roles.",
        "aliases": ["pyspark", "apache spark"],
        "resources": [
            {"title": "Spark Quick Start (PySpark)", "platform": "Official Docs", "url": "https://spark.apache.org/docs/latest/api/python/getting_started/index.html", "type": "docs", "free": True, "difficulty": "advanced", "hours": 10},
        ],
    },
    {
        "key": "aws", "name": "Cloud Basics (AWS)", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 25,
        "description": "S3, Athena, SageMaker notebooks and moving analysis into the cloud.",
        "why_important": "Analytics infrastructure has moved to cloud warehouses; AWS leads.",
        "aliases": ["amazon web services", "aws cloud"],
        "resources": [
            {"title": "AWS Get Started Guides", "platform": "Official Docs", "url": "https://aws.amazon.com/getting-started/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "business-acumen", "name": "Business Domain Knowledge", "category": "domain", "level": "intermediate",
        "priority": "must_have", "hours": 20,
        "description": "Unit economics, funnels, retention cohorts and framing analysis around KPIs.",
        "why_important": "Analyses land only when tied to metrics leadership cares about.",
        "aliases": ["business intelligence", "domain knowledge", "product analytics"],
        "resources": [
            {"title": "Google Data Analytics Professional Certificate", "platform": "Coursera (audit free)", "url": "https://www.coursera.org/professional-certificates/google-data-analytics", "type": "certification", "free": False, "difficulty": "beginner", "hours": 180},
        ],
    },
    {
        "key": "communication", "name": "Communication & Storytelling", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 12,
        "description": "Executive summaries, narrative structure and presenting uncertainty without losing clarity.",
        "why_important": "Insight that isn't communicated doesn't exist.",
        "aliases": ["storytelling", "presentation skills", "communication skills"],
        "resources": [
            {"title": "Storytelling with Data", "platform": "Book — Wiley", "url": "", "type": "book", "free": False, "difficulty": "beginner", "hours": 8},
        ],
    },
    {
        "key": "problem-solving", "name": "Problem Solving", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 0,
        "description": "Structured hypothesis trees, MECE decomposition and prioritizing by impact.",
        "why_important": "Case interviews test structured thinking before technical depth.",
        "aliases": ["analytical thinking", "critical thinking"],
        "resources": [
            {"title": "Case Interview Prep", "platform": "Khan Academy (free MCAT-style practice)", "url": "https://www.khanacademy.org/", "type": "practice", "free": True, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "llms-rag", "name": "LLMs for Analytics", "category": "technical", "level": "advanced",
        "priority": "recommended", "hours": 18,
        "description": "Using LLMs for text summarization pipelines, semantic search over feedback and AI-assisted analysis.",
        "why_important": "Fastest-emerging expectation on modern DS job descriptions.",
        "aliases": ["large language models", "llm", "generative ai", "genai"],
        "resources": [
            {"title": "Prompt Engineering Guide", "platform": "DAIR.AI", "url": "https://www.promptingguide.ai/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "cert-google-data-analytics", "name": "Google Data Analytics Certificate", "category": "certification", "level": "optional",
        "priority": "optional", "hours": 60,
        "description": "Entry-level credential covering the full analytics workflow end-to-end.",
        "why_important": "Recognized entry credential for career switchers into analytics.",
        "aliases": [],
        "resources": [
            {"title": "Google Data Analytics Professional Certificate", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/google-data-analytics", "type": "certification", "free": False, "difficulty": "beginner", "hours": 180},
        ],
    },
]

EDGES = [
    ("python", "numpy"), ("numpy", "pandas"), ("pandas", "eda"),
    ("pandas", "matplotlib"), ("python", "pandas"),
    ("statistics", "machine-learning"), ("eda", "machine-learning"),
    ("machine-learning", "scikit-learn"), ("scikit-learn", "feature-engineering"),
    ("statistics", "a-b-testing"), ("a-b-testing", "time-series"),
    ("eda", "nlp-basics"), ("nlp-basics", "llms-rag"),
    ("python", "spark"), ("sql", "spark"),
    ("aws", "spark"),
    ("matplotlib", "tableau"), ("matplotlib", "power-bi"),
    ("machine-learning", "business-acumen"),
    ("git", "python"),
    ("cert-google-data-analytics", "sql"),
]
