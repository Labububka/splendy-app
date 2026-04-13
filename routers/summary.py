from fastapi import APIRouter, Depends
from typing import Optional
from auth_helpers import get_current_user
import services.summary_service as summary_service

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/weekly")
def weekly_summary(week_start: Optional[str] = None, user_id: int = Depends(get_current_user)):
    return summary_service.get_weekly(user_id, week_start)


@router.get("/monthly")
def monthly_summary(month: Optional[str] = None, user_id: int = Depends(get_current_user)):
    return summary_service.get_monthly(user_id, month)


@router.get("/insights")
def insights(user_id: int = Depends(get_current_user)):
    return summary_service.get_insights(user_id)
