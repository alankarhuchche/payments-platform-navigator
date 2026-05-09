# Payments Platform Navigator Frontend

React TypeScript frontend for the Payments Platform Navigator MVP.

The frontend consumes the deterministic FastAPI backend and presents role-based onboarding, payment flow exploration, service dependency context, rule-based Ask the Platform, change-safety checklist generation, knowledge-health metrics, and glossary search.

## Local Setup

```bash
cd frontend
npm install
```

## Backend Dependency

Start the backend first:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

The frontend expects the backend API at:

```text
http://localhost:8080
```

Override with:

```bash
VITE_API_BASE_URL=http://localhost:8080 npm run dev
```

## Run

```bash
cd frontend
npm run dev
```

## Build

```bash
cd frontend
npm run build
```

## Notes

- No authentication is implemented in the MVP.
- No database or external AI integration is used.
- All visible data comes from the synthetic backend API.
- Routing uses browser hash state to keep the first frontend implementation simple.
