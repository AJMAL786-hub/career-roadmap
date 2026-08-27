# CareerPath AI ??

An AI-powered developer career roadmap and skill mastery platform. Choose your tech track, master interactive skill Directed Acyclic Graphs (DAGs), close job description skill gaps with ATS analysis, practice technical interviews, build portfolio projects, and log study sessions.

---

## ? Quick Start

To launch both backend and frontend simultaneously with a single click:

### Option 1: One-Click Launcher (Windows)
Double-click **`start.bat`** or **`run.bat`** in the project root directory.

---

### Option 2: Manual Start

#### 1. Start the Backend API (FastAPI)
```bash
cd backend
py -3.10 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Documentation (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

#### 2. Start the Frontend (Vite + React)
```bash
cd frontend
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## ?? Demo Account Credentials
The application automatically logs in with a pre-configured demo account for instant access:
- **Email:** `alex.chen@example.com`
- **Password:** `password123`

---

## ??? Features & Modules
- **Interactive Skill DAG Roadmaps:** Visual skill dependencies, prerequisite unlock trees, and progress tracking.
- **Job Description Gap Analyzer:** Match job descriptions against current verified skill sets.
- **ATS Resume Keyword Scanner:** Identify high-impact missing keywords and receive targeted bullet point optimizations.
- **Interactive Interview Arena:** Practice DSA, System Design, and domain questions with built-in timer and answer guides.
- **Portfolio Project Hub:** Tiered projects with milestone checklists, deliverables, and rubric validation.
- **Focus Study Timer & Pomodoro:** Log study sessions, track daily streaks, and earn XP badges.
- **Market Intelligence:** Real-time hiring demand index, tech stack adoption metrics, and salary ranges.
