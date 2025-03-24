# Django Blog Project

A blog application built with Django that allows users to read blog posts, view author details, and comment on posts.

## Features

- View all blog posts with pagination
- View individual blog post details
- View author profiles and their posts
- Comment on blog posts (requires login)
- Admin interface for managing content

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Testing

Run the test suite:
```bash
python manage.py test
``` 