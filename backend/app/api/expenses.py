from fastapi import APIRouter, File, UploadFile

from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/api/expenses", tags=["expenses"])
service = ExpenseService()


@router.post("/import/csv")
def import_csv(file: UploadFile = File(...)):
    content = file.file.read()
    return service.import_csv(content)


@router.post("/import/excel")
def import_excel(file: UploadFile = File(...)):
    content = file.file.read()
    return service.import_excel(content)


@router.get("/summary")
def summary():
    return service.summary()


@router.post("/budget")
def set_budget(category: str, limit: float, month: str | None = None):
    return service.set_budget(category, limit, month)


@router.get("/dashboard")
def dashboard():
    summary = service.summary()
    return {
        "transaction_count": summary["transaction_count"],
        "total_spending": summary["total_spending"],
        "monthly_summary": summary["monthly_summary"],
        "category_breakdown": summary.get("category_breakdown", []),
        "trend_series": summary.get("trend_series", []),
        "budget_status": summary.get("budget_status", []),
        "duplicate_candidates": summary.get("duplicate_candidates", []),
        "monthly_change": summary.get("monthly_change", []),
        "insights": summary.get("insights", []),
    }
