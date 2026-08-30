from http import HTTPStatus

from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from dependencies.dashboard import get_dashboard_service
from schemas.dashboard_schema import (
    DashboardAnalysis,
    DashboardCategory,
    DashboardFilter,
    DashboardHistory,
    DashboardSummary,
)
from services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
    status_code=HTTPStatus.OK,
)
def get_summary(
    filters: DashboardFilter = Depends(),
    service: DashboardService = Depends(get_dashboard_service),
    current_user=Depends(get_current_user),
):
    return service.get_summary(
        user_id=current_user.id,
        start_date=filters.start_date,
        end_date=filters.end_date,
    )


@router.get(
    "/category",
    response_model=list[DashboardCategory],
    status_code=HTTPStatus.OK,
)
def get_category(
    filters: DashboardFilter = Depends(),
    service: DashboardService = Depends(get_dashboard_service),
    current_user=Depends(get_current_user),
):
    return service.get_category_summary(
        user_id=current_user.id,
        start_date=filters.start_date,
        end_date=filters.end_date,
    )


@router.get(
    "/history",
    response_model=list[DashboardHistory],
    status_code=HTTPStatus.OK,
)
def get_history(
    filters: DashboardFilter = Depends(),
    service: DashboardService = Depends(get_dashboard_service),
    current_user=Depends(get_current_user),
):
    return service.get_history(
        user_id=current_user.id,
        start_date=filters.start_date,
        end_date=filters.end_date,
    )


@router.get(
    "/analysis",
    response_model=DashboardAnalysis,
    status_code=HTTPStatus.OK,
)
def get_analysis(
    filters: DashboardFilter = Depends(),
    service: DashboardService = Depends(get_dashboard_service),
    current_user=Depends(get_current_user),
):
    return service.get_analysis(
        user_id=current_user.id,
        start_date=filters.start_date,
        end_date=filters.end_date,
    )
