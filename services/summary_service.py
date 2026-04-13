from datetime import date, timedelta, datetime
import repositories.summary_repository as summary_repo

SMALL_PURCHASE_CATEGORIES = ('Coffee', 'Delivery', 'Food')


def validate_month(month: str):
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("Invalid month format. Use YYYY-MM")


def validate_date(date_str: str):
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")


def get_weekly(user_id: str, week_start: str = None):
    if not week_start:
        today = date.today()
        week_start = (today - timedelta(days=today.weekday())).isoformat()
    week_end = (validate_date(week_start) + timedelta(days=6)).isoformat()
    rows = summary_repo.get_weekly_breakdown(user_id, week_start, week_end)
    return {
        "week_start": week_start,
        "week_end": week_end,
        "total": sum(r["total"] for r in rows),
        "by_category": rows
    }


def get_monthly(user_id: str, month: str = None):
    if not month:
        month = date.today().strftime("%Y-%m")
    validate_month(month)
    rows = summary_repo.get_monthly_breakdown(user_id, month)
    return {
        "month": month,
        "total": sum(r["total"] for r in rows),
        "by_category": rows
    }


def get_insights(user_id: str):
    today = date.today()
    week_start = (today - timedelta(days=today.weekday())).isoformat()
    rows = summary_repo.get_small_purchases(user_id, week_start, SMALL_PURCHASE_CATEGORIES)
    return {
        "week_start": week_start,
        "invisible_spending_total": sum(r["total"] for r in rows),
        "breakdown": rows
    }
