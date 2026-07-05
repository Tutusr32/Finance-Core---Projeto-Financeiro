from fastapi import FastAPI

from controllers.users_controller import router as users_router
from controllers.accounts_controller import router as accounts_router
from controllers.transactions_controller import router as transactions_router

app = FastAPI(title="Finance Core")

app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
