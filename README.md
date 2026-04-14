# SaaS Platform — Senior FullStack Takeover

Flask + Vue3 + PostgreSQL + Docker + AWS SaaS application.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 22+ (for frontend development)
- Python 3.12+ (for backend development)

### Local Development

```bash
# Start all services
docker-compose up -d

# Backend (Flask)
cd server
pip install -r requirements.txt
python app.py

# Frontend (Vue 3)
cd client
npm install
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and configure:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — Flask secret key
- `JWT_SECRET_KEY` — JWT signing secret

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.x, SQLAlchemy, Alembic |
| Frontend | Vue 3, Vite, Pinia, Tailwind |
| Database | PostgreSQL 16 |
| Container | Docker, docker-compose |
| Cloud | AWS EC2, RDS, S3, CloudWatch |

## API Endpoints

- `POST /api/auth/register` — User registration
- `POST /api/auth/login` — User login
- `GET /api/auth/me` — Current user info
- `GET /api/users` — List users (admin)
- `PUT /api/users/:id` — Update user
- `GET /api/dashboard/stats` — Dashboard statistics
- `GET /api/subscriptions/plans` — List plans
- `POST /api/subscriptions/` — Create subscription
- `POST /api/subscriptions/:id/cancel` — Cancel subscription

## Project Structure

```
├── server/          # Flask backend
│   ├── app.py       # Application factory
│   ├── config.py    # Configuration
│   ├── models/      # SQLAlchemy models
│   ├── routes/      # API blueprints
│   └── services/    # Business logic
├── client/          # Vue 3 frontend
│   └── src/
│       ├── views/   # Page components
│       ├── composables/  # Vue composables
│       └── router.js
└── docker-compose.yml
```

## License

MIT
