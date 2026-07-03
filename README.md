# Insurance Management System

A Django-based insurance management application with modules for accounts, policies, premiums, and claims.

## Features

- **Accounts**: User authentication and management
- **Policies**: Insurance policy management
- **Premium**: Premium payment tracking
- **Claims**: Claims processing and management

## Tech Stack

- Django 6.0.4
- Python 3.x
- SQLite (development) / PostgreSQL (production)
- Gunicorn (production server)
- Whitenoise (static file serving)

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd insurance
```

2. Create a virtual environment:
```bash
python -m venv env
```

3. Activate the virtual environment:

**Windows:**
```bash
env\Scripts\activate
```

**Mac/Linux:**
```bash
source env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Environment Variables

Create a `.env` file in the project root (optional for local development):

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Project Structure

```
insurance/
├── accounts/          # User authentication module
├── claims/            # Claims management module
├── policies/          # Policy management module
├── premium/           # Premium payment module
├── insurance/         # Main Django project settings
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── Procfile          # Process configuration for Render
├── render.yaml       # Render deployment configuration
└── .gitignore        # Git ignore rules
```

## Deployment on Render

This project is configured for easy deployment on Render using the provided `render.yaml` file.

### Automatic Deployment (Recommended)

1. Push your code to GitHub
2. In Render dashboard, create a new "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and configure everything
5. Deploy

### Manual Deployment

If you prefer manual configuration, use these settings in Render dashboard:

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

**Start Command:**
```
gunicorn insurance.wsgi:application
```

**Environment Variables:**
- `SECRET_KEY`: Generate a secure random string
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `.onrender.com` (or your custom domain)
- `DATABASE_URL`: Auto-populated if using Render PostgreSQL

### Database

The project uses SQLite for local development and PostgreSQL for production. The `render.yaml` file includes a PostgreSQL database configuration that will be automatically created.

## Production Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use PostgreSQL database (configured in render.yaml)
- [ ] Ensure static files are collected during build

## License

This project is licensed under the MIT License.
