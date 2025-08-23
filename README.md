# Trip Planner

A web-based Trip Planner platform that helps users organize and document their travels.

## Features
*   Plan future trips with details, to-do lists, and photos.
*   Document past trips with memory collages and reviews.
*   User profiles and authentication.

## Tech Stack
*   Backend: Django, Django REST Framework
*   Database: SQLite (Development)
*   Frontend: React (Planned)

## Installation
1.  Clone the repository: `git clone <your-repo-url>`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the environment: `.\venv\Scripts\Activate.ps1`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run migrations: `python manage.py migrate`
6.  Start the server: `python manage.py runserver`

## Project Structure
trip-planner/
├── core/ # Django project settings
│ ├── init.py
│ ├── settings.py # Project settings (e.g., INSTALLED_APPS, Databases)
│ ├── urls.py # Main URL routing configuration
│ ├── asgi.py # ASGI config for deployment
│ └── wsgi.py # WSGI config for deployment
├── trips/ # Main app: Handles trip planning and memories
│ ├── migrations/ # Database migration files (auto-generated)
│ ├── init.py
│ ├── admin.py # Register models for Django admin interface
│ ├── apps.py # App configuration
│ ├── models.py # Database models (e.g., Trip model)
│ ├── tests.py # App-specific tests
│ └── views.py # App logic/views (Future API endpoints)
├── users/ # App: Handles user accounts and profiles
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ └── views.py
├── venv/ # Virtual environment (ignored by Git)
├── db.sqlite3 # SQLite database file (ignored by Git)
├── .gitignore # Files to ignore in version control
├── requirements.txt # Project dependencies (Django, etc.)
├── manage.py # Django's command-line utility
└── README.md # This file