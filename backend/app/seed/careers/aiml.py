"""AI/ML Engineer career seed data: skills, DAG edges, resources."""

CAREER = {
    "slug": "ai-ml-engineer",
    "title": "AI/ML Engineer",
    "description": (
        "Design, train, and deploy machine learning systems — from classical ML "
        "pipelines to production LLM applications. Blends software engineering, "
        "mathematics, and data intuition."
    ),
    "icon": "brain-circuit",
    "color": "#8b5cf6",
    "difficulty": "advanced",
    "typical_roles": ["ML Engineer", "AI Engineer", "Applied Scientist", "MLOps Engineer", "LLM Engineer"],
    "major_technologies": ["Python", "PyTorch", "TensorFlow", "scikit-learn", "Docker", "AWS", "Hugging Face"],
}

# key, name, category, level, priority, hours, aliases
SKILLS = [
    {
        "key": "python", "name": "Python", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 60,
        "description": "The lingua franca of AI/ML. Master syntax, data structures, OOP, virtual environments and the scientific stack.",
        "why_important": "Nearly every ML framework, library, and job posting centers on Python.",
        "aliases": ["Python 3", "Python programming", "python scripting"],
        "resources": [
            {"title": "Official Python Tutorial", "platform": "Official Docs", "url": "https://docs.python.org/3/tutorial/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 15},
            {"title": "Scientific Computing with Python", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "type": "course", "free": True, "difficulty": "beginner", "hours": 300},
            {"title": "Automate the Boring Stuff with Python", "platform": "Book (free online)", "url": "https://automatetheboringstuff.com/", "type": "book", "free": True, "difficulty": "beginner", "hours": 20},
        ],
    },
    {
        "key": "linear-algebra-calculus", "name": "Linear Algebra & Calculus", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 45,
        "description": "Vectors, matrices, eigenvalues, gradients and chain rule — the mathematics underneath every model.",
        "why_important": "Understanding gradients and matrix operations is essential to debug and design models.",
        "aliases": ["linear algebra", "matrix algebra", "calculus"],
        "resources": [
            {"title": "Essence of Linear Algebra", "platform": "3Blue1Brown (YouTube)", "url": "https://www.youtube.com/@3blue1brown/playlists", "type": "video", "free": True, "difficulty": "beginner", "hours": 6},
            {"title": "Linear Algebra (18.06)", "platform": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", "type": "course", "free": True, "difficulty": "intermediate", "hours": 60},
        ],
    },
    {
        "key": "statistics", "name": "Statistics & Probability", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 50,
        "description": "Descriptive stats, distributions, hypothesis testing, Bayes theorem and uncertainty quantification.",
        "why_important": "Models are statistical estimators; you must reason about variance, bias and significance.",
        "aliases": ["statistics & probability", "probability & statistics", "statistical analysis"],
        "resources": [
            {"title": "Statistics and Probability", "platform": "Khan Academy", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "course", "free": True, "difficulty": "beginner", "hours": 40},
            {"title": "StatQuest with Josh Starmer", "platform": "YouTube", "url": "https://www.youtube.com/@statquest", "type": "video", "free": True, "difficulty": "beginner", "hours": 20},
        ],
    },
    {
        "key": "sql", "name": "SQL", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 30,
        "description": "Joins, aggregations, window functions and query optimization for extracting training data.",
        "why_important": "Training data lives in databases; extracting it efficiently is a daily task.",
        "aliases": ["structured query language"],
        "resources": [
            {"title": "SQLBolt Interactive Lessons", "platform": "SQLBolt", "url": "https://sqlbolt.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 8},
            {"title": "Advanced SQL Tutorial", "platform": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "type": "tutorial", "free": True, "difficulty": "intermediate", "hours": 12},
        ],
    },
    {
        "key": "git", "name": "Git & Version Control", "category": "tool", "level": "fundamental",
        "priority": "must_have", "hours": 10,
        "description": "Branching, merging, rebasing, pull requests and collaborative workflows on GitHub.",
        "why_important": "All modern engineering teams collaborate through version control.",
        "aliases": ["github", "version control"],
        "resources": [
            {"title": "Pro Git (official book)", "platform": "git-scm.com", "url": "https://git-scm.com/book/en/v2", "type": "book", "free": True, "difficulty": "beginner", "hours": 12},
            {"title": "Learn Git Branching", "platform": "learngitbranching.js.org", "url": "https://learngitbranching.js.org/", "type": "practice", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "linux", "name": "Linux & Shell", "category": "tool", "level": "fundamental",
        "priority": "recommended", "hours": 18,
        "description": "Filesystem, permissions, processes, SSH, and bash scripting for GPU boxes and servers.",
        "why_important": "Model training happens on Linux servers; comfort in the terminal is non-negotiable.",
        "aliases": ["linux administration", "bash", "shell scripting"],
        "resources": [
            {"title": "Linux Journey", "platform": "linuxjourney.com", "url": "https://linuxjourney.com/", "type": "tutorial", "free": True, "difficulty": "beginner", "hours": 12},
            {"title": "The Linux Command Line (book)", "platform": "Official", "url": "http://linuxcommand.org/tlcl.php", "type": "book", "free": True, "difficulty": "beginner", "hours": 25},
        ],
    },
    {
        "key": "numpy", "name": "NumPy", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 22,
        "description": "Vectorized computation, broadcasting, and N-dimensional arrays — the substrate of ML math.",
        "why_important": "Every tensor library builds on NumPy concepts; vectorization is how Python stays fast.",
        "aliases": [],
        "resources": [
            {"title": "NumPy: The Absolute Basics", "platform": "Official Docs", "url": "https://numpy.org/doc/stable/user/absolute_beginners.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "pandas", "name": "Pandas", "category": "technical", "level": "fundamental",
        "priority": "must_have", "hours": 30,
        "description": "DataFrames, group-by, joins, time series handling and cleaning messy tabular data.",
        "why_important": "80% of applied ML time is data loading, cleaning, and transformation.",
        "aliases": [],
        "resources": [
            {"title": "Pandas Getting Started", "platform": "Official Docs", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "matplotlib", "name": "Matplotlib & Seaborn", "category": "technical", "level": "fundamental",
        "priority": "recommended", "hours": 14,
        "description": "Plotting distributions, losses, confusion matrices and embeddings for analysis and debugging.",
        "why_important": "Visual diagnosis of data and model behavior guides every modeling decision.",
        "aliases": ["seaborn", "data visualization"],
        "resources": [
            {"title": "Matplotlib Tutorials", "platform": "Official Docs", "url": "https://matplotlib.org/stable/tutorials/index.html", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
            {"title": "Kaggle Learn: Data Visualization", "platform": "Kaggle", "url": "https://www.kaggle.com/learn/data-visualization", "type": "course", "free": True, "difficulty": "beginner", "hours": 4},
        ],
    },
    {
        "key": "machine-learning", "name": "Machine Learning", "category": "technical", "level": "intermediate",
        "priority": "must_have", "hours": 85,
        "description": "Supervised/unsupervised learning, bias-variance tradeoff, regularization, evaluation metrics, cross-validation.",
        "why_important": "The core discipline: choosing, training, and validating models that generalize.",
        "aliases": ["ml", "applied machine learning", "classical ml"],
        "resources": [
            {"title": "Machine Learning Specialization (Andrew Ng)", "platform": "Coursera (audit free)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "course", "free": False, "difficulty": "beginner", "hours": 90},
            {"title": "Introduction to ML Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "course", "free": True, "difficulty": "beginner", "hours": 3},
        ],
    },
    {
        "key": "scikit-learn", "name": "scikit-learn", "category": "framework", "level": "intermediate",
        "priority": "must_have", "hours": 35,
        "description": "Pipelines, transformers, model selection, metrics — the standard toolkit for classical ML.",
        "why_important": "Industry-standard API for classical ML; appears in most DS/ML interviews.",
        "aliases": ["sklearn"],
        "resources": [
            {"title": "scikit-learn Tutorials", "platform": "Official Docs", "url": "https://scikit-learn.org/stable/tutorial/index.html", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "feature-engineering", "name": "Feature Engineering", "category": "technical", "level": "intermediate",
        "priority": "recommended", "hours": 25,
        "description": "Encoding categoricals, scaling, target leakage detection, and domain-driven feature creation.",
        "why_important": "Better features routinely beat fancier models on real tabular problems.",
        "aliases": [],
        "resources": [
            {"title": "Feature Engineering Course", "platform": "Kaggle Learn", "url": "https://www.kaggle.com/learn/feature-engineering", "type": "course", "free": True, "difficulty": "intermediate", "hours": 5},
        ],
    },
    {
        "key": "deep-learning", "name": "Deep Learning", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 70,
        "description": "Backpropagation, CNNs, RNNs, optimizers, regularization, transfer learning and training dynamics.",
        "why_important": "Foundation for computer vision, NLP, and every modern generative model.",
        "aliases": ["neural networks", "dl"],
        "resources": [
            {"title": "Practical Deep Learning for Coders", "platform": "fast.ai", "url": "https://course.fast.ai/", "type": "course", "free": True, "difficulty": "intermediate", "hours": 70},
            {"title": "Deep Learning Specialization", "platform": "Coursera (audit free)", "url": "https://www.coursera.org/specializations/deep-learning", "type": "course", "free": False, "difficulty": "intermediate", "hours": 120},
        ],
    },
    {
        "key": "pytorch", "name": "PyTorch", "category": "framework", "level": "advanced",
        "priority": "must_have", "hours": 45,
        "description": "Tensors, autograd, nn.Module, DataLoaders, distributed training and custom architectures.",
        "why_important": "Dominant research framework; required by most cutting-edge teams.",
        "aliases": ["torch"],
        "resources": [
            {"title": "PyTorch Official Tutorials", "platform": "Official Docs", "url": "https://pytorch.org/tutorials/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 20},
        ],
    },
    {
        "key": "tensorflow", "name": "TensorFlow / Keras", "category": "framework", "level": "advanced",
        "priority": "optional", "hours": 40,
        "description": "Keras model building, tf.data pipelines, and TensorFlow Serving for production inference.",
        "why_important": "Widely used in enterprise production environments, especially Google Cloud shops.",
        "aliases": ["tf", "keras", "tensorflow 2"],
        "resources": [
            {"title": "TensorFlow Tutorials", "platform": "Official Docs", "url": "https://www.tensorflow.org/tutorials", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 15},
        ],
    },
    {
        "key": "nlp", "name": "NLP Fundamentals", "category": "technical", "level": "advanced",
        "priority": "recommended", "hours": 35,
        "description": "Tokenization, embeddings, sequence models, text classification and language modeling basics.",
        "why_important": "Language is the dominant modality of modern AI applications.",
        "aliases": ["natural language processing", "text processing"],
        "resources": [
            {"title": "NLP Course", "platform": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "type": "course", "free": True, "difficulty": "intermediate", "hours": 25},
        ],
    },
    {
        "key": "transformers", "name": "Transformers", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 40,
        "description": "Self-attention, encoder/decoder stacks, fine-tuning BERT/GPT families, PEFT and LoRA.",
        "why_important": "The architecture behind GPT, Claude, Llama and virtually all frontier models.",
        "aliases": ["transformer models", "hugging face transformers", "attention mechanism"],
        "resources": [
            {"title": "Hugging Face Learn Hub", "platform": "Hugging Face", "url": "https://huggingface.co/learn", "type": "course", "free": True, "difficulty": "advanced", "hours": 30},
        ],
    },
    {
        "key": "llms-rag", "name": "LLMs & RAG", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 45,
        "description": "Prompt engineering, retrieval-augmented generation, agents, evals and guardrails for LLM apps.",
        "why_important": "The fastest-growing skill demand in AI hiring since 2023.",
        "aliases": ["large language models", "llm", "rag", "retrieval augmented generation", "generative ai", "genai", "gen ai", "prompt engineering"],
        "resources": [
            {"title": "LangChain Documentation", "platform": "LangChain", "url": "https://python.langchain.com/docs/introduction/", "type": "docs", "free": True, "difficulty": "advanced", "hours": 15},
            {"title": "OpenAI Cookbook", "platform": "OpenAI", "url": "https://cookbook.openai.com/", "type": "github", "free": True, "difficulty": "advanced", "hours": 10},
        ],
    },
    {
        "key": "vector-databases", "name": "Vector Databases", "category": "tool", "level": "advanced",
        "priority": "recommended", "hours": 12,
        "description": "Embedding storage, ANN indexes (HNSW), similarity search and hybrid retrieval.",
        "why_important": "Core infrastructure of every RAG system.",
        "aliases": ["vector database", "embeddings store", "faiss"],
        "resources": [
            {"title": "Chroma Documentation", "platform": "Chroma", "url": "https://docs.trychroma.com/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 4},
        ],
    },
    {
        "key": "computer-vision", "name": "Computer Vision", "category": "technical", "level": "advanced",
        "priority": "optional", "hours": 40,
        "description": "Image classification, object detection, segmentation and vision transformers.",
        "why_important": "High-demand specialty across automotive, retail analytics and healthcare imaging.",
        "aliases": ["cv", "image processing"],
        "resources": [
            {"title": "CS231n: Deep Learning for Computer Vision", "platform": "Stanford", "url": "https://cs231n.stanford.edu/", "type": "course", "free": True, "difficulty": "advanced", "hours": 60},
            {"title": "OpenCV Documentation", "platform": "OpenCV", "url": "https://docs.opencv.org/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 10},
        ],
    },
    {
        "key": "docker", "name": "Docker", "category": "tool", "level": "intermediate",
        "priority": "must_have", "hours": 20,
        "description": "Images, containers, Dockerfiles, compose and reproducible training/serving environments.",
        "why_important": "Reproducibility and deployment both run through containers.",
        "aliases": ["containerization", "containers"],
        "resources": [
            {"title": "Docker Get Started", "platform": "Official Docs", "url": "https://docs.docker.com/get-started/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 6},
        ],
    },
    {
        "key": "kubernetes", "name": "Kubernetes", "category": "tool", "level": "advanced",
        "priority": "recommended", "hours": 35,
        "description": "Pods, deployments, services, autoscaling GPU workloads and Helm packaging.",
        "why_important": "Large-scale model serving platforms are Kubernetes-based.",
        "aliases": ["k8s", "kubernetes orchestration"],
        "resources": [
            {"title": "Kubernetes Tutorials", "platform": "Official Docs", "url": "https://kubernetes.io/docs/tutorials/", "type": "docs", "free": True, "difficulty": "advanced", "hours": 12},
        ],
    },
    {
        "key": "aws", "name": "AWS (Cloud)", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 40,
        "description": "EC2/SageMaker/S3/Lambda fundamentals for training jobs and model endpoints.",
        "why_important": "AWS leads cloud market share; SageMaker endpoints appear everywhere in JDs.",
        "aliases": ["amazon web services", "aws cloud", "sagemaker", "ec2", "s3", "lambda", "aws lambda"],
        "resources": [
            {"title": "AWS Training and Certification", "platform": "AWS Skill Builder", "url": "https://aws.amazon.com/training/", "type": "course", "free": True, "difficulty": "beginner", "hours": 20},
            {"title": "AWS Get Started Guides", "platform": "Official Docs", "url": "https://aws.amazon.com/getting-started/", "type": "docs", "free": True, "difficulty": "beginner", "hours": 10},
        ],
    },
    {
        "key": "fastapi", "name": "FastAPI", "category": "framework", "level": "intermediate",
        "priority": "recommended", "hours": 18,
        "description": "Async Python APIs, Pydantic validation and serving ML models over HTTP.",
        "why_important": "De-facto framework for wrapping models as microservices.",
        "aliases": [],
        "resources": [
            {"title": "FastAPI Tutorial (User Guide)", "platform": "Official Docs", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "model-deployment", "name": "Model Deployment", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 30,
        "description": "Packaging models as APIs, batch vs real-time inference, A/B rollouts and latency budgets.",
        "why_important": "A model that isn't deployed creates zero business value.",
        "aliases": ["model serving"],
        "resources": [
            {"title": "Full Stack Deep Learning: Deployment", "platform": "FSDL", "url": "https://fullstackdeeplearning.com/course/2022/", "type": "course", "free": True, "difficulty": "advanced", "hours": 30},
        ],
    },
    {
        "key": "mlops", "name": "MLOps", "category": "technical", "level": "advanced",
        "priority": "must_have", "hours": 40,
        "description": "Experiment tracking, model registry, CI/CD for ML, drift monitoring and reproducible pipelines.",
        "why_important": "Companies need people who can keep models healthy in production, not just train them.",
        "aliases": ["ml ops", "machine learning operations"],
        "resources": [
            {"title": "Made With ML", "platform": "madewithml.com", "url": "https://madewithml.com/", "type": "course", "free": True, "difficulty": "advanced", "hours": 40},
            {"title": "MLflow Documentation", "platform": "MLflow", "url": "https://mlflow.org/docs/latest/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 8},
        ],
    },
    {
        "key": "spark", "name": "Apache Spark", "category": "tool", "level": "advanced",
        "priority": "optional", "hours": 35,
        "description": "Distributed DataFrame processing with PySpark for datasets beyond single-machine memory.",
        "why_important": "Required when training data outgrows one machine; common in big-data teams.",
        "aliases": ["pyspark", "apache spark"],
        "resources": [
            {"title": "Spark Quick Start (PySpark)", "platform": "Official Docs", "url": "https://spark.apache.org/docs/latest/api/python/getting_started/index.html", "type": "docs", "free": True, "difficulty": "advanced", "hours": 10},
        ],
    },
    {
        "key": "airflow", "name": "Airflow", "category": "tool", "level": "intermediate",
        "priority": "optional", "hours": 25,
        "description": "Authoring DAGs, scheduling retraining pipelines and orchestrating data dependencies.",
        "why_important": "Retraining pipelines must run reliably on schedule; Airflow is the default orchestrator.",
        "aliases": ["apache airflow"],
        "resources": [
            {"title": "Airflow Documentation & Tutorial", "platform": "Official Docs", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 10},
        ],
    },
    {
        "key": "ci-cd", "name": "CI/CD Pipelines", "category": "tool", "level": "intermediate",
        "priority": "recommended", "hours": 18,
        "description": "Automated test/build/deploy pipelines with GitHub Actions or GitLab CI.",
        "why_important": "Continuous delivery of models and code separates hobby projects from production.",
        "aliases": ["cicd", "ci cd", "continuous integration", "github actions", "gitlab ci"],
        "resources": [
            {"title": "GitHub Actions Documentation", "platform": "GitHub Docs", "url": "https://docs.github.com/en/actions", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
        ],
    },
    {
        "key": "ai-ethics", "name": "AI Ethics & Responsible AI", "category": "domain", "level": "intermediate",
        "priority": "recommended", "hours": 12,
        "description": "Fairness metrics, model cards, privacy, explainability and responsible deployment practices.",
        "why_important": "Regulatory scrutiny (EU AI Act) makes responsible-AI literacy a hiring filter.",
        "aliases": ["responsible ai", "fairness in ai", "explainability"],
        "resources": [
            {"title": "People + AI Guidebook", "platform": "Google PAIR", "url": "https://pair.withgoogle.com/guidebook", "type": "docs", "free": True, "difficulty": "beginner", "hours": 5},
            {"title": "Fairlearn Documentation", "platform": "Fairlearn", "url": "https://fairlearn.org/", "type": "docs", "free": True, "difficulty": "intermediate", "hours": 4},
        ],
    },
    {
        "key": "communication", "name": "Communication", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 10,
        "description": "Explaining model trade-offs to stakeholders, writing clear docs and presenting results.",
        "why_important": "ML value is realized only when non-technical stakeholders understand and trust results.",
        "aliases": ["communication skills"],
        "resources": [
            {"title": "Storytelling with Data", "platform": "Book — Wiley", "url": "", "type": "book", "free": False, "difficulty": "beginner", "hours": 8},
        ],
    },
    {
        "key": "problem-solving", "name": "Problem Solving", "category": "soft_skill", "level": "fundamental",
        "priority": "must_have", "hours": 0,
        "description": "Decomposing ambiguous business problems into tractable ML formulations.",
        "why_important": "Interviewers probe structured thinking harder than any specific library.",
        "aliases": ["analytical thinking", "critical thinking"],
        "resources": [
            {"title": "LeetCode Problem Sets", "platform": "LeetCode", "url": "https://leetcode.com/problemset/", "type": "practice", "free": True, "difficulty": "intermediate", "hours": 50},
        ],
    },
    {
        "key": "cert-tensorflow-developer", "name": "TensorFlow Developer Certificate", "category": "certification", "level": "optional",
        "priority": "optional", "hours": 50,
        "description": "Official TensorFlow proficiency certificate covering CNNs, NLP and time series in Keras.",
        "why_important": "Signals hands-on TF ability to employers who use the Google ecosystem.",
        "aliases": ["tensorflow certificate"],
        "resources": [
            {"title": "TensorFlow Developer Certificate Program", "platform": "TensorFlow", "url": "https://www.tensorflow.org/certificate", "type": "certification", "free": False, "difficulty": "intermediate", "hours": 50},
        ],
    },
    {
        "key": "cert-aws-ml-specialty", "name": "AWS Certified Machine Learning – Specialty", "category": "certification", "level": "optional",
        "priority": "optional", "hours": 70,
        "description": "Validates building, training and deploying ML models on AWS at production scale.",
        "why_important": "Strong signal for ML roles at AWS-heavy enterprises.",
        "aliases": ["aws ml certification", "aws machine learning specialty"],
        "resources": [
            {"title": "AWS ML Specialty Exam Guide", "platform": "AWS", "url": "https://aws.amazon.com/certification/certified-machine-learning-specialty/", "type": "certification", "free": True, "difficulty": "advanced", "hours": 70},
        ],
    },
]

EDGES = [
    ("python", "numpy"), ("numpy", "pandas"), ("pandas", "matplotlib"),
    ("python", "machine-learning"), ("linear-algebra-calculus", "machine-learning"),
    ("statistics", "machine-learning"), ("pandas", "machine-learning"),
    ("numpy", "deep-learning"),
    ("machine-learning", "scikit-learn"), ("scikit-learn", "feature-engineering"),
    ("machine-learning", "deep-learning"),
    ("deep-learning", "pytorch"), ("deep-learning", "tensorflow"),
    ("pytorch", "transformers"), ("nlp", "transformers"),
    ("machine-learning", "nlp"),
    ("transformers", "llms-rag"), ("llms-rag", "vector-databases"),
    ("deep-learning", "computer-vision"),
    ("linux", "docker"), ("docker", "kubernetes"),
    ("python", "fastapi"), ("fastapi", "model-deployment"),
    ("docker", "model-deployment"), ("aws", "model-deployment"),
    ("docker", "mlops"), ("machine-learning", "mlops"), ("ci-cd", "mlops"),
    ("python", "spark"), ("sql", "spark"), ("python", "airflow"),
    ("python", "ci-cd"), ("git", "ci-cd"), ("aws", "linux"),
    ("machine-learning", "ai-ethics"),
    ("tensorflow", "cert-tensorflow-developer"),
    ("aws", "cert-aws-ml-specialty"), ("machine-learning", "cert-aws-ml-specialty"),
]
