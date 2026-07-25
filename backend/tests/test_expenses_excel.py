from io import BytesIO

from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.main import app


client = TestClient(app)


def test_excel_import_creates_transactions():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["date", "description", "amount", "category"])
    sheet.append(["2026-07-03", "Rent", 1200.00, "Housing"])
    sheet.append(["2026-07-04", "Internet", 50.00, "Utilities"])

    excel_bytes = BytesIO()
    workbook.save(excel_bytes)
    excel_bytes.seek(0)

    response = client.post(
        "/api/expenses/import/excel",
        files={"file": ("transactions.xlsx", excel_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["imported_count"] == 2
