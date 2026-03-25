# HRMS Lite API – Backend

Django REST Framework backend for the HRMS Lite (Human Resource Management System) application.

---

## Project Overview

Provides a REST API for managing employee records and daily attendance tracking. Built with Django and Django REST Framework, backed by MySQL, deployed on Render.

---

## Tech Stack

| Purpose | Technology |
|---|---|
| Framework | Django 6.0.3 |
| REST API | Django REST Framework 3.17 |
| CORS | django-cors-headers |
| Static Files | WhiteNoise |
| WSGI Server | Gunicorn |
| Database | MySQL (via mysqlclient) |
| Deployment | Railway |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/employees/` | List all employees |
| POST | `/api/employees/` | Create a new employee |
| GET | `/api/employees/{id}/` | Retrieve an employee |
| PUT | `/api/employees/{id}/` | Update an employee |
| DELETE | `/api/employees/{id}/` | Delete an employee |
| GET | `/api/employees/dashboard/` | Dashboard summary stats |
| GET | `/api/attendance/` | List attendance records |
| POST | `/api/attendance/` | Mark attendance |
| PUT | `/api/attendance/{id}/` | Update attendance record |
| DELETE | `/api/attendance/{id}/` | Delete attendance record |

**Attendance query parameters:**
- `?employee={id}` — filter by employee
- `?date=YYYY-MM-DD` — filter by exact date
- `?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD` — filter by date range

**Employee query parameters:**
- `?search={term}` — search by name, employee ID, or department

---

## Running Locally

### Prerequisites

- Python 3.9+
- pip
- MySQL 8.0+ running locally
  - Create a database: `CREATE DATABASE hrms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/your-username/hrms-lite-api.git
cd hrms-lite-api

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env — set SECRET_KEY, DEBUG=True, and MYSQL_* connection details

# 5. Run migrations
python manage.py migrate

# 6. Start the development server
python manage.py runserver
```

API is available at **http://localhost:8000/api/**

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | Insecure fallback (dev only) |
| `DEBUG` | Enable debug mode | `False` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |
| `MYSQL_DATABASE` | MySQL database name | `hrms` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | `` |
| `MYSQL_HOST` | MySQL host | `localhost` |
| `MYSQL_PORT` | MySQL port | `3306` |

---

## Deployment (Railway)

Railway natively supports MySQL — no external database service needed.

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. Click **Add Plugin** → select **MySQL** — Railway provisions it and injects env vars automatically
4. Add these environment variables in Railway dashboard:
   - `SECRET_KEY` → any strong random string
   - `DEBUG` → `False`
   - `CORS_ALLOWED_ORIGINS` → your Vercel frontend URL (e.g. `https://hrms-lite.vercel.app`)
5. Railway auto-detects the `Procfile` and runs migrate + collectstatic + gunicorn on deploy

Railway injects MySQL connection as: `MYSQLHOST`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`, `MYSQLPORT` — settings.py reads these automatically.

---

## Project Structure

```
.
├── backend/            # Django project settings, URLs, WSGI
├── employees/          # Main app
│   ├── models.py       # Employee & Attendance models
│   ├── serializers.py  # DRF serializers with validation
│   ├── views.py        # ViewSets with custom actions
│   └── urls.py         # Router config
├── manage.py
├── requirements.txt
├── Procfile            # Railway start command
├── railway.json        # Railway config
└── build.sh            # Optional Render build script
```

---

## Assumptions & Limitations

- No authentication — single admin user (per project scope)
- MySQL is required both locally and in production
- On Render's free tier, the MySQL database plan provides persistent storage