from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.dashboard_repository import DashboardRepository
from services.dashboard_service import DashboardService


def get_dashboard_repository(
    db: Session = Depends(get_db),
):
    return DashboardRepository(db)


def get_dashboard_service(
    repo: DashboardRepository = Depends(get_dashboard_repository),
):
    return DashboardService(repo)
