# SaaS Platform - Flask + Vue3 + Docker

Full-stack SaaS platform with Flask backend and Vue3 frontend.

## Tech Stack

- **Backend**: Python 3.12, Flask 3.0, SQLAlchemy, JWT authentication
- **Frontend**: Vue 3, Vite, Pinia, Tailwind CSS
- **Database**: PostgreSQL 16
- **Container**: Docker & Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Setup

**Backend:**
```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/saas_db
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users` - List users (paginated)
- `GET /api/users/<id>` - Get user details
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (admin only)

### Dashboard
- `GET /api/dashboard/stats` - Get platform statistics
- `GET /api/dashboard/activity` - Get audit log activity

### Subscriptions
- `GET /api/subscriptions` - List subscriptions
- `POST /api/subscriptions` - Create subscription
- `GET /api/subscriptions/plans` - List available plans

## Environment Variables

See `.env.example` for required environment variables.

## Project Structure

```
├── app/
│   ├── models/       # SQLAlchemy models
│   ├── routes/       # API route handlers
│   └── services/     # Business logic services
├── frontend/
│   └── src/
│       ├── views/    # Vue components
│       ├── stores/    # Pinia stores
│       └── composables/  # Vue composables
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
