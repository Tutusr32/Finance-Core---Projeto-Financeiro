from contextlib import asynccontextmanager

from fastapi import FastAPI

from controllers.accounts_controller import router as accounts_router
from controllers.auth_controller import router as auth_router
from controllers.dashboard_controller import router as dashboard_router
from controllers.recurring_transaction_controller import router as recurring_transaction_router
from controllers.transactions_controller import router as transactions_router
from controllers.users_controller import router as users_router
from core.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="Finance Core", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(dashboard_router)
app.include_router(recurring_transaction_router)
