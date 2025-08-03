# AI Assistant Django App with Google OAuth & OpenAI Chat Integration

This project is a Django-based AI assistant web application that supports:
- Email/password authentication and Google OAuth login
- OPENROUTER API integration for natural language conversations
- Chat interface with Bootstrap-based frontend UI
- Google Calendar and Gmail API access via user-authenticated OAuth tokens


> **Use the following test account to log in via Google:**

- 📧 Email: `demo.assigntest@gmail.com`
- 🔐 Password: `demo@123`

##  Project Structure

```
.
├── .env                       # Environment variables
├── .gitignore
├── client_secret.json        # Google OAuth client credentials
├── db.sqlite3                # SQLite DB (for demo purposes)
├── manage.py                 # Django management script
├── requirements.txt
├── structure.txt             # Folder tree dump
├── backend/                  # Django project settings and config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __pycache__/
├── core/                     # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── integration_registry.py
│   ├── models.py
│   ├── oauth.py              # Google OAuth logic
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── __pycache__/
├── templates/                # HTML templates
│   ├── base.html
│   ├── chat.html
│   ├── login.html
│   └── register.html
```

## 🚀 Features

- 🔐 Google OAuth2 login (using `google-auth-oauthlib`)
- ✉️ Gmail API & 📆 Google Calendar API access (via OAuth tokens)
- 🤖 OPENROUTER chat integration using `gpt-3.5-turbo`
- 🧠 Extensible tool system via `integration_registry.py`
- 🧪 SQLite database, compatible with PostgreSQL for production
- 🧼 Clean Bootstrap 5 frontend with chat UI

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/ai-assistant-django.git
cd ai-assistant-django
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run Migrations**

```bash
python manage.py migrate
```

5. **Run the Server**

```bash
python manage.py runserver
```

## ✅ Test User Access (for OAuth)

- Add test user emails in Google OAuth test users section.
- Alternatively, share demo login credentials with email/password from the Django admin panel.

