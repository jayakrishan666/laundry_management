# Laundry Management System

A modern web application for managing laundry services with user and admin interfaces.

## Features

- User Registration and Authentication
- Laundry Item Management
- Laundry Request System
- Admin Dashboard
- Status Tracking
- Email Notifications
- Responsive Design
- Modern UI/UX

## Tech Stack

- Python 3.x
- Django 5.x
- SQLite (Development) / PostgreSQL (Production)
- HTML5 / CSS3 / JavaScript
- Bootstrap 5

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jayakrishan666/laundry_management.git
cd laundry-management
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following:
```
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
laundry_management/
├── laundry/                 # Main application
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── static/            # Static files (CSS, JS, images)
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin configuration
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Deployment

### Local Deployment

1. Follow the installation instructions above
2. Run the development server:
```bash
python manage.py runserver
```
3. Access the application at `http://localhost:8000`

### Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Configure environment variables:
```bash
heroku config:set DJANGO_SETTINGS_MODULE=laundry_management.settings
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

5. Deploy the application:
```bash
git push heroku main
```

6. Run migrations:
```bash
heroku run python manage.py migrate
```

7. Create superuser:
```bash
heroku run python manage.py createsuperuser
```

## Usage

### User Interface

1. Register a new account
2. Log in to your account
3. Browse available laundry items
4. Select items and specify quantities
5. Submit laundry request
6. Track request status
7. Provide feedback

### Admin Interface

1. Log in as admin
2. Access admin dashboard
3. Manage laundry items
4. Update request status
5. View user feedback
6. Monitor system activity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@example.com or create an issue in the repository.
