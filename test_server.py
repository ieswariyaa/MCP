import pytest
import database
import server

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    path=tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", path)
    database.create_database(path)

def test_add_expense_ok():
    result = server.add_expense("Lunch", 150, "Food", "2026-10-18")
    assert "added" in result

def test_negative_amount_rejected():
    with pytest.raises(ValueError):
        server.add_expense("Lunch", -5, "Food", "2026-10-18")

def test_bad_date_rejected():
    with pytest.raises(ValueError):
        server.add_expense("Lunch", 100, "Food", "18-10-2026")

def test_monthly_total():
    server.add_expense("Lunch", 100, "food", "2026-10-01")
    server.add_expense("Bus", 50, "travel", "2026-10-02")
    server.add_expense("Old", 999, "food", "2026-09-01")
    assert "150" in server.monthly_total("2026-10")

def test_bad_month_rejected():
    with pytest.raises(ValueError):
        server.monthly_total("October")

def test_top_categories():
    server.add_expense("Lunch", 100, "food", "2026-10-01")
    server.add_expense("Bus", 50, "travel", "2026-10-02")
    result = server.top_categories("2026-10", 1)
    assert "food" in result and "travel" not in result