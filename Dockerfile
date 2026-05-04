FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend ./
RUN npm run build

FROM python:3.11-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

ENV PORT=8000
ENV PYTHONPATH=/app/backend

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
