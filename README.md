# Library Management System

Django + DRF based API for managing books, loans, and authentication with JWT tokens. Users can register, browse/filter/paginate the catalog, borrow and return books, while librarians/admin staff manage inventory through the API or Django admin.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# optional mock data
python manage.py seed_library
```

- API root: `http://127.0.0.1:8000/api/`
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- Redoc: `http://127.0.0.1:8000/redoc/`
- Django admin: `http://127.0.0.1:8000/admin/`

### Env Vars (`.env`)

| Variable                                      | Description                                                     |
| --------------------------------------------- | --------------------------------------------------------------- |
| `DJANGO_SECRET_KEY`                           | Django secret key.                                              |
| `DJANGO_DEBUG`                                | `true/false`.                                                   |
| `DJANGO_ALLOWED_HOSTS`                        | Comma-separated host list.                                      |
| `DATABASE_URL`                                | PostgreSQL URL (Heroku style). Falls back to SQLite if omitted. |
| `DATABASE_SSL_REQUIRE`                        | `true` to enforce Postgres SSL.                                 |
| `ACCESS_TOKEN_MINUTES` / `REFRESH_TOKEN_DAYS` | JWT lifetimes.                                                  |

## Running Tests

```bash
source .venv/bin/activate
pytest
```

Coverage is reported automatically (configured via `pytest.ini`).

## Docker

```bash
docker compose up --build
```

- Database: Postgres service exposed on `localhost:5432`.
- Web service reachable at `http://127.0.0.1:8000/`.
- Copy `.env.example` to `.env`
- Containers automatically run `python manage.py migrate` on startup (see `entrypoint.sh`), but you can still run admin commands manually with `docker compose exec web ...`.

## API Highlights

- `POST /api/auth/register/` – register a new account.
- `POST /api/auth/token/` & `/api/auth/token/refresh/` – obtain/refresh JWTs.
- `GET /api/books/` – list books (anonymous allowed), supports search/filter/order/pagination.
- `POST /api/books/` – create books (staff/librarians only).
- `POST /api/books/{id}/borrow/` – borrow a book (authenticated).
- `POST /api/books/{id}/return/` – return a book (self or specify `user_id` if staff/librarian).
- `GET /api/loans/` – view your active & past loans (staff/librarian see all).
