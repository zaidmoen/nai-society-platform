# NAI Society Platform

Administrative platform for Najah AI Society, built with Django REST Framework and React.

## Product scope

- Manage association members, committee assignments, and role requests.
- Plan events and volunteer shifts; volunteers submit availability and committee coordinators confirm assignments.
- Record attendance, committee notes, and periodic volunteer evaluations.
- Track treasury records with restricted access.
- Support the five current committees: Activities, Technical, Media, Public Relations, and Specialized AI Activities.

This repository starts with the product foundation: an Arabic RTL React admin prototype and a Django API/data-model scaffold. The current frontend uses sample data so the design can be reviewed before connecting it to a live database.

## API foundation

- `GET /api/health/`
- `GET /api/committees/`
- `GET /api/events/` (published events for visitors; committee drafts are scoped to authorized coordinators)
- `GET, POST /api/availability/` and `PATCH /api/availability/{id}/` for a volunteer's own availability
- `POST /api/availability/{id}/confirm/` for an authorized committee lead or volunteer manager
- `GET, POST /api/evaluations/` and `/api/committee-notes/`, scoped to the evaluating committee
- `/api/finance/transactions/` for authorized treasury and executive roles; `/approve/` and `/reject/` actions require an executive approver
- `POST /api/auth/register/` creates a disabled, pending account request. Staff approve the requested role from Django Admin.
- `GET, POST /api/auth/session/` and `GET /api/auth/csrf/` provide session-based authentication and CSRF bootstrap.

Create the five current committees after migrating the backend with `python manage.py seed_committees`.

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, Lucide icons.
- Backend: Django, Django REST Framework, PostgreSQL-ready settings.

## Run locally

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

SQLite is used by default for local development. Set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` to use PostgreSQL.

## Security/product decisions

- Account registration requests access; it never grants a privileged role by itself.
- Role assignments and committee memberships must be approved by an authorized administrator.
- Availability means a volunteer is available; a coordinator must confirm the shift.
- Evaluation records are scoped to the evaluating committee and are not a public leaderboard.
- Day-to-day task coordination remains outside the platform; WhatsApp stays the team's working channel.

## Current committees

1. Activities
2. Technical
3. Media
4. Public Relations
5. Specialized AI Activities
