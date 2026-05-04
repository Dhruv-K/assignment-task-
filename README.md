# Team Task Manager

Full-stack team task management app with role-based access control.

## Features

- User signup and login with JWT auth
- Projects with admin and member roles
- Task creation, assignment, and status tracking
- Dashboard with projects and tasks
- Single Dockerized service deployable on Railway

## Tech Stack

- Backend: FastAPI, PostgreSQL, SQLAlchemy, JWT
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Deployment: Docker and Railway

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost:5432/team_task_manager
export JWT_SECRET_KEY=change-me
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env` with:

```env
VITE_API_URL=http://localhost:8000
```

## Docker

```bash
docker build -t team-task-manager .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:pass@host:5432/db -e JWT_SECRET_KEY=change-me team-task-manager
```

## Railway Deployment

1. Create a PostgreSQL database on Railway.
2. Copy the `DATABASE_URL`.
3. Create a new service from your GitHub repo.
4. Set `DATABASE_URL` and `JWT_SECRET_KEY` as environment variables.
5. Deploy using the root Dockerfile.

## Demo Video

- Show signup and login
- Create a project
- Open the project and add tasks
- Change task status across Todo, In Progress, and Done
- Show the live Railway deployment
