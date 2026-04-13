# Splendy API

A minimal REST API for the Splendy student expense tracker app, built with FastAPI and SQLite.

## Project Structure

```
project/
├── main.py
├── database.py
├── auth_helpers.py
├── constants.py
├── dtos/
│   ├── auth_dto.py
│   ├── expense_dto.py
│   ├── category_dto.py
│   └── user_dto.py
├── routers/
│   ├── auth.py
│   ├── expenses.py
│   ├── categories.py
│   ├── summary.py
│   └── users.py
├── services/
│   ├── auth_service.py
│   ├── expense_service.py
│   ├── category_service.py
│   ├── summary_service.py
│   └── user_service.py
└── repositories/
    ├── user_repository.py
    ├── expense_repository.py
    ├── category_repository.py
    └── summary_repository.py
```

## Requirements

- Python 3.10+
- fastapi
- uvicorn
- pyjwt

## Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/splendy-api.git
cd splendy-api
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

3. Install dependencies
```bash
pip install fastapi uvicorn pyjwt
```

4. Create a `.env` file in the root directory
```bash
SECRET_KEY=your-secret-key-here
```

5. Run the server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs are available at `http://localhost:8000/docs`.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing secret | `splendy-secret-key` |

## API Reference

### Auth

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive a token | No |
| POST | `/auth/logout` | Logout | Yes |

### Expenses

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/expenses` | List expenses (filterable by date, category) | Yes |
| POST | `/expenses` | Log a new expense | Yes |
| PUT | `/expenses/{id}` | Update an expense | Yes |
| DELETE | `/expenses/{id}` | Delete an expense | Yes |

### Categories

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/categories` | List all categories | Yes |
| POST | `/categories` | Create a custom category | Yes |
| DELETE | `/categories/{id}` | Delete a custom category | Yes |

### Summary

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/summary/weekly` | Weekly spending breakdown by category | Yes |
| GET | `/summary/monthly` | Monthly spending breakdown by category | Yes |
| GET | `/summary/insights` | Invisible spending breakdown (coffee, delivery, food) | Yes |

### Users

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/users/me` | Get current user profile | Yes |
| PUT | `/users/me` | Update current user profile | Yes |

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your-token>
```

You receive the token after registering or logging in.

## Default Categories

The following categories are available to all users out of the box:
`Food`, `Transport`, `Fun`, `Coffee`, `Delivery`, `Other`

Custom categories can be created per user and deleted freely. Default categories cannot be deleted.

## Validation Rules

### User
- **Name**: 2–100 characters
- **Email**: valid email format, lowercased on save
- **Password**: min 8 characters, at least one uppercase letter and one digit
- **Currency**: one of `UAH`, `USD`, `EUR`, `GBP`

### Expense
- **Amount**: greater than 0, at most 1,000,000, rounded to 2 decimal places
- **Date**: `YYYY-MM-DD` format, cannot be in the future
- **Note**: at most 255 characters

### Category
- **Name**: 2–100 characters, cannot duplicate a default category

## Architecture

The project follows a layered architecture:

- **Routers** — handle HTTP requests and responses only
- **DTOs** — define and validate request shapes using Pydantic
- **Services** — contain business logic and raise HTTP exceptions
- **Repositories** — handle all database queries, no logic
- **Constants** — shared constants used across multiple files
