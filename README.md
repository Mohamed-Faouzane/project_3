# Note REST API

A production-grade REST API built with FastAPI and PostgreSQL.

## Stack
- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM (Object Relational Mapper)
- **JWT** — authentication
- **Alembic** — migrations

## Auth
- `POST /users/rergister` — create account
- `POST /users/login` — get JWT token

### Notes (requires auth)
- `Get /notes/` — list your notes
- `POST /notes/` — create a note
- `GET /notes/{id}` — get one note
- `PUT /notes/{id}` — update a note
- `DELETE /notes/{id}` — delete a note

## Running locally

```bash
pythpn -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs