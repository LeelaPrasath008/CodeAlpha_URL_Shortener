# URL Shortener

A Flask-based URL Shortener developed as part of the CodeAlpha Backend Development Internship.

## Features

- Generate short URLs
- Redirect to original URLs
- SQLite database storage
- URL validation
- Collision prevention
- Click tracking analytics
- Responsive frontend interface

## Tech Stack

- Python
- Flask
- SQLite
- SQLAlchemy
- HTML
- CSS
- JavaScript

## Installation

```bash
pip install -r requirements.txt
python app.py
```

## Project Workflow

1. User enters a URL
2. Flask validates the URL
3. System generates a unique short code
4. URL mapping is stored in SQLite
5. User accesses short URL
6. System redirects to original URL
7. Click count is updated

## Author

Leelaprasath V