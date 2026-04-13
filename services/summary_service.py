from datetime import date, timedelta
import repositories.summary_repository as summary_repo

SMALL_PURCHASE_CATEGORIES = ('Coffee', 'Delivery', 'Food')


def get_weekly(user_id: int, week_start: str = None):
    if not week_start:
        today = date.today()
        week_start = (today - timedelta(days=today.weekday())).isoformat()
    week_end = (date.fromisoformat(week_start) + timedelta(days=6)).isoformat()
    rows = summary_repo.get_weekly_breakdown(user_id, week_start, week_end)
    return {
        "week_start": week_start,
        "week_end": week_end,
        "total": sum(r["total"] for r in rows),
        "by_category": rows
    }


def get_monthly(user_id: int, month: str = None):
    if not month:
        month = date.today().strftime("%Y-%m")
    rows = summary_repo.get_monthly_breakdown(user_id, month)
    return {
        "month": month,
        "total": sum(r["total"] for r in rows),
        "by_category": rows
    }


def get_insights(user_id: int):
    today = date.today()
    week_start = (today - timedelta(days=today.weekday())).isoformat()
    rows = summary_repo.get_small_purchases(user_id, week_start, SMALL_PURCHASE_CATEGORIES)
    return {
        "week_start": week_start,
        "invisible_spending_total": sum(r["total"] for r in rows),
        "breakdown": rows
    }
