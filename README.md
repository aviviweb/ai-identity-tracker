AI Identity Tracker – Hybrid Intelligence System

Overview

This monorepo hosts a hybrid intelligence system that analyzes public social media data (text, images, activity patterns) to detect bot/fake accounts and correlate identities across profiles. It includes a Next.js frontend, FastAPI backend, PostgreSQL database, and a modular AI Investigator. Supports Demo Mode (seeded data) and Live Mode (future API integrations).

Modules

- frontend/ — Next.js (App Router) + Tailwind CSS + charts
- backend/ — FastAPI + SQLAlchemy + Alembic + JWT auth (HttpOnly cookies)
- ai/ — AI Investigator placeholders (text/image/correlation)
- database/ — Migrations and seed scripts
- infra/ — Dev tooling (optional docker compose)
- env/ — Environment examples

Quick start (development)

Prerequisites

- Node.js 18+
- Python 3.11+
- Windows PowerShell (for provided scripts)

Backend setup (one time)

1. Create virtualenv and install deps:
   - In `backend/`: `py -3.11 -m venv .venv` then `.\.venv\Scripts\python.exe -m pip install -U pip` and `.\.venv\Scripts\python.exe -m pip install -U -e .`
2. Env variables:
   - Copy `env/backend.env.example` to `backend/.env` (or rely on shell env). Ensure `DATABASE_URL=sqlite:///C:/dev/ai-identity-tracker/dev.db`.
3. Initialize DB and seed demo:
   - From repo root: `backend\.venv\Scripts\python.exe database\seed\ensure_db.py` then `backend\.venv\Scripts\python.exe database\seed\seed_demo.py`.

Run services

- One command (recommended): `infra\dev.ps1` (starts API on 127.0.0.1:8001 and Next.js on 3000)
- Manual:
  - Backend: `setx JWT_SECRET dev-secret-change` (optional), then in `backend/`: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001`
  - Frontend: in `frontend/`: `npm install` then `npm run dev` (port 3000)

Configuration

- Frontend API base: `frontend/.env.local` → `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001`
- CORS: `env/backend.env.example` includes ports 3000/5001

Testing

- Backend smoke tests: in `backend/`: `.\.venv\Scripts\python.exe -m pytest`
- Frontend build check: in `frontend/`: `npm run build`

Endpoints

- Health: `GET /health`
- Auth: `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`
- Profiles: `GET /profiles?mode=demo|live`
- Analysis: `POST /analysis/text`, `POST /analysis/image`, `POST /analysis/correlate`, `POST /analysis/run`
- Results: `GET /results`, `GET /results/{id}`, `GET /results/{id}/export?format=json|csv`
- History: `GET /history?limit=20&offset=0&action=&user_id=`

Security and scope

- Only public data is analyzed. No private data collection.
- Demo Mode uses seeded fake profiles to ensure safe testing.

License

MIT


Troubleshooting

- Uvicorn ModuleNotFoundError: No module named 'ai'
  - Always run the API from the repo (or `backend/`) after installing in editable mode: `backend\\.venv\\Scripts\\python.exe -m pip install -U -e backend/`
  - Ensure you created `backend/.venv` and are using that interpreter.
  - `backend/app/__init__.py` adds the repo root to `sys.path`; if you moved directories, re-run install.

- Browser CORS errors
  - Update `env/backend.env.example` → `CORS_ORIGINS` to include your frontend origin (e.g. `http://localhost:3000`).
  - Restart the API after changing env variables.

- Frontend can’t reach API
  - Set `frontend/.env.local` → `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001`.
  - Confirm API is running: `GET http://127.0.0.1:8001/health` should return `{ "status": "ok" }`.

- SQLite lock errors on Windows
  - Close any tools holding the DB file (`dev.db`). Stop the API, then retry.

- CSV export downloads as JSON
  - The `/results/{id}/export?format=csv` endpoint currently returns `{ format, content }` (JSON). Copy the `content` string or use the JSON export. Native file download headers can be added later if needed.

- Next.js port mismatch
  - Dev server runs on port 3000 (standardized). If you used port 5001, update `CORS_ORIGINS` and restart.

