# Event Management API

Event Management REST API built using **Django 5+**, **Django REST Framework**, and **PostgreSQL**, containerized with **Docker**,
This project supports creating events, managing registrations, and handling user authentication.

---

## Features
- Create and manage **events**
- Register and manage **participants**
- Secure **JWT Authentication**
- Restful API with **Django REST Framework**
- **PostgreSQL** database
- **Dockersied** setup for easy deployment

---

## Tech Stack
- **Python 3.11**
- **Django 5.0+**
- **Django REST Framework**
- **PostgreSQL 14**
- **JWT Authentication**
- **Gunicorn** (WSGI)
- **Docker** & **Docker Compose**

---

## Project Structure

```bash
event-management-app/
├─ apps/
│  ├─ core/
│  ├─ events/
│  ├─ registrations/
│  └─ users/
├─ config/
└─ static/
└─ tests/
│  ├─ test_registration.py
├─ .env
├─ .env.docker
├─ docker-compose.yml
├─ Dockerfile
├─ manage.py
├─ README.md
├─ requirements.txt
```

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/fajarpostman/event-management-app.git
cd event-management-app
```

### 2. Create .env.docker
```bash
DATABASE_NAME=event_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
DEBUG=True
SECRET_KEY=your_secret_key_here
```

### 3. Build and run with Docker
```bash
docker-compose up --build
access app at: http://localhost:8000
```

### 4. Local setup (Manual/Python Vitualenv)
```bash
python -m venv .venv
source venv/bin/activate # on macOS/Linux
venv\Scripts\activate # on Windows
```

### 5. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Setup Environment Variables
Create .env file in the root directory:
```bash
DEBUG=True
SECRET_KEY=change_me
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_NAME=event_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 7. Run Database Migrations
```bash
python manage.py migrate
```

### 8. Create superuser
```bash
python manage.py createsuperuser
```

### 9. Run the Development Server
```bash
python manage.py runserver
```

### 10. Access the application
- Django API: http://localhost:8000
---

## Docker Setup

### 1. Build and Run Containers
```bash
docker-compose up --build
```

### 2. Apply Migrations (if not auto-applied)
```bash
docker-compose exec web python manage.py migrate
```

### 3. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Access the Application
- Django API: http://localhost:8000
- PostgreSQL: exposed on port 5432

---

## Testing Instructions


You can run the test suite using Django's test runner or pytest:
```bash
dokcer-compose excec web python manage.py test
```

Or using pytest:
```bash
docker-compose exec web pytest
```

On python test
---

### API Endpoints Overview

| Endpoint               | Method           | Description                          | Auth |
| ---------------------- | ---------------- | ------------------------------------ | ---- |
| `/api/events/`         | GET, POST        | List or create events                | ✅    |
| `/api/events/{id}/`    | GET, PUT, DELETE | Retrieve, update, or delete an event | ✅    |
| `/api/sessions/`       | GET, POST        | Manage sessions within events        | ✅    |
| `/api/tracks/`         | GET, POST        | Manage tracks                        | ✅    |
| `/api/registrations/`  | POST             | Register attendee for an event       | ✅    |
| `/api/users/register/` | POST             | Create a new user account            | ❌    |
| `/api/auth/token/`     | POST             | Obtain JWT token                     | ❌    |

More detail you can check Swagger or Redoc

- Redoc:
```bash
http://localhost:8000/api/docs/redoc/
```

- Swagger:
```bash
http://localhost:8000/api/docs/swagger/
```

---

---

## License

This project is licensed under the MIT license.

---

## Author
**Fajar Dwi Rianto**
📧 fajardwirianto3@gmail.com
🌐 github.com/fajarpostman