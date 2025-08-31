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


## API End points and JSON body Examples
## Authentication & User Management

Register a new user
**POST** http://127.0.0.1:8000/api/register/  
**JSON Body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "strongpassword123"
}
Login
POST http://127.0.0.1:8000/api/login/
JSON Body:

json
Copy code
{
  "username": "alice",
  "password": "strongpassword123"
}
Logout
POST http://127.0.0.1:8000/api/logout/
JSON Body:

json
Copy code
{
  "refresh": "your_refresh_token_here"
}
Get Profile
GET http://127.0.0.1:8000/api/profile/
JSON Body: Empty

Update Profile
PATCH http://127.0.0.1:8000/api/profile/
JSON Body:

json
Copy code
{
  "username": "alice_new",
  "email": "alice_new@example.com",
  "bio": "I love traveling and exploring new places"
}

Future & Past Trips
Create a new trip
POST http://127.0.0.1:8000/api/trips/
JSON Body:

json
Copy code
{
  "title": "Rome Vacation",
  "location": "Rome",
  "start_date": "2025-09-10",
  "end_date": "2025-09-17",
  "trip_type": "Couple",
  "notes": "Looking forward to museums and good food",
  "status": "Future",
  "budget_range": "Medium"
}
List all trips
GET http://127.0.0.1:8000/api/trips/
JSON Body: Empty

Get trip details
GET http://127.0.0.1:8000/api/trips/{trip_id}/
JSON Body: Empty

Update trip
PATCH http://127.0.0.1:8000/api/trips/{trip_id}/
JSON Body:

json
Copy code
{
  "notes": "Had an amazing time visiting museums",
  "review": "Best trip ever!",
  "budget_range": "High",
  "favorite_moments": [
    {"description": "Eiffel Tower at sunset"},
    {"description": "Seine river cruise"}
  ],
  "status": "Completed"
}
Delete a trip
DELETE http://127.0.0.1:8000/api/trips/{trip_id}/
JSON Body: Empty

Mark trip as complete
POST http://127.0.0.1:8000/api/trips/{trip_id}/mark-complete/
JSON Body: Empty

To-Do List (for Future Trips)
Add a to-do item
POST http://127.0.0.1:8000/api/trips/{trip_id}/todos/
JSON Body:

json
Copy code
{
  "task_descri": "Book museum tickets"
}
List to-do items
GET http://127.0.0.1:8000/api/trips/{trip_id}/todos/
JSON Body: Empty

Update a to-do item
PATCH http://127.0.0.1:8000/api/todos/{todo_id}/
JSON Body:

json
Copy code
{
  "task_descri": "Buy tickets online instead",
  "is_complete": true
}
Delete a to-do item
DELETE http://127.0.0.1:8000/api/todos/{todo_id}/
JSON Body: Empty

Photos (Inspirations or Memories)
Upload a photo
POST http://127.0.0.1:8000/api/trips/{trip_id}/photos/
JSON Body:

json
Copy code
{
  "image": "<base64_or_file_upload_here>",
  "description": "Sunset at the Colosseum"
}
Get all photos
GET http://127.0.0.1:8000/api/trips/{trip_id}/photos/
JSON Body: Empty

Delete a photo
DELETE http://127.0.0.1:8000/api/photos/{photo_id}/
JSON Body: Empty

Favorite Moments (Past Trips)
Add a favorite moment
POST http://127.0.0.1:8000/api/trips/{trip_id}/favorite_moments/
JSON Body:

json
Copy code
{
  "description": "Walking along the Seine at night"
}

Social Features
Follow a user
POST http://127.0.0.1:8000/api/follow/{user_id}/
JSON Body: Empty

Unfollow a user
DELETE http://127.0.0.1:8000/api/unfollow/{user_id}/
JSON Body: Empty

List followers
GET http://127.0.0.1:8000/api/followers/{user_id}/
JSON Body: Empty

List following
GET http://127.0.0.1:8000/api/following/{user_id}/
JSON Body: Empty

Search users
GET http://127.0.0.1:8000/api/users/?search=<query>
JSON Body: Empty

View Others’ Shared Trips
View completed trips of another user
GET http://127.0.0.1:8000/api/users/{user_id}/trips/
JSON Body: Empty

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