# SE_MiniProject_Team9

Blood Bank Management System (BBMS) — a student Software Engineering mini-project by Team 9.

Manages donor registration, blood donation recording, real-time inventory tracking, and blood unit search, built with Django REST Framework and a vanilla JavaScript frontend.

## Team

| Name | USN | Role |
|------|-----|------|
| Ritesh Kumar Sharma | PES2UG24CS404 | Accounts, Donations, Inventory, Frontend |
| Reyansh | PES2UG24CS401 | Security (password hashing, JWT), Docs |
| Ritesh Babu Reddy | PES2UG24CS403 | Blood Search, RBAC |
| Rithish P M | PES2UG24CS405 | Project skeleton, CI/CD |

## Quick Start (local development)

```bash
# 1. Clone the repo
git clone https://github.com/ritesh-shar/SE_MiniProject_Team9.git
cd SE_MiniProject_Team9

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the environment file
cp .env.example .env

# 5. Run database migrations
python manage.py migrate

# 6. (Optional) Seed demo data for a quick walkthrough
python manage.py seed_demo

# 7. Start the development server
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.
Open `frontend/index.html` in a browser for the web client.

## Running Tests

```bash
python manage.py test
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register a new donor |
| POST | `/api/auth/login` | Login (returns JWT) |
| POST | `/api/auth/token/refresh` | Refresh an expired access token |
| POST | `/api/donations` | Record a blood donation (Staff/Admin) |
| GET | `/api/donations/history` | View donation history |
| GET | `/api/inventory` | View current blood stock levels |
| GET | `/api/inventory/search?bloodGroup=&component=` | Search blood units |

## Project Structure

```
├── accounts/      # User registration, login, JWT, RBAC permissions
├── donations/     # Donation recording, 90-day eligibility rule
├── inventory/     # Blood stock tracking, search
├── frontend/      # HTML/CSS/JS web client
├── docs/          # Project documentation
└── bbms/          # Django project settings
```

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Auth:** JWT (djangorestframework-simplejwt)
- **Database:** SQLite (local dev), PostgreSQL (production)
- **Frontend:** HTML, CSS, vanilla JavaScript
- **CI:** GitHub Actions
