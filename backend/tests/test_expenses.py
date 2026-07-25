from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_csv_import_creates_transactions():
    csv_content = "date,description,amount\n2026-07-01,Grocery shopping,45.50\n2026-07-02,Utility bill,80.00\n"
    response = client.post(
        "/api/expenses/import/csv",
        files={"file": ("transactions.csv", BytesIO(csv_content.encode("utf-8")), "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["imported_count"] == 2
    assert payload["categories_created"] >= 1


def test_summary_endpoint_returns_monthly_breakdown():
    response = client.get("/api/expenses/summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["transaction_count"] >= 2
    assert payload["total_spending"] >= 125.5
    assert len(payload["monthly_summary"]) >= 1


def test_budget_endpoint_sets_budget_limit():
    response = client.post(
        "/api/expenses/budget",
        params={"category": "Groceries", "limit": 300.0, "month": "2026-07"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "Groceries"
    assert payload["limit"] == 300.0
    assert payload["month"] == "2026-07"
