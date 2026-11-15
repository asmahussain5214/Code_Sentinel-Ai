# CodeSentinel AI

AI-Powered Code Review, Bug Detection & Security Analysis Platform.

## Overview
CodeSentinel AI is a developer tool that analyzes Python codebases for:
- Static Code Quality & Linting
- Security Vulnerabilities (SAST)
- Cyclomatic Complexity & Maintainability
- Deterministic AST Pattern Matching
- AI-Powered Vulnerability Explanations & Remediation Guidance

## Technology Stack
- **Backend:** Python 3.14, FastAPI, SQLAlchemy, oracledb
- **Static Analyzers:** Python `ast`, Ruff, Bandit, Radon
- **Database:** Oracle Database 23c / 26ai
- **Frontend:** React, Vite, Tailwind CSS
- **AI Engine:** External LLM Integration


  ## 🚀 How to Run CodeSentinel AI Locally

**1. Activate Virtual Environment (Project Root)**
```powershell
.\.venv\Scripts\Activate.ps1
```

**2. Start Backend (Terminal 1)**
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```


**3. Start Frontend (New Terminal – Terminal 2)**
```powershell
cd frontend
npm run dev
```
Open The url -You can see application 

**Note:** Ensure Node.js, npm, and project dependencies are installed. If frontend dependencies are not installed, run `npm install` inside the frontend directory before `npm run dev`. Keep both terminals running while using the application.
