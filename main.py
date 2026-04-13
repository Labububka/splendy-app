from fastapi import FastAPI
from database import init_db
from routers import auth, expenses, categories, summary, users

app = FastAPI()
init_db()

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)
app.include_router(summary.router)
app.include_router(users.router)