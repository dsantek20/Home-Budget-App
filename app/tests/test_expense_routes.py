from decimal import Decimal
from uuid import uuid4
import pytest
from utils.datetime_helpers import get_current_date, get_past_date

pytestmark = pytest.mark.asyncio 


class TestGetExpenseById:

    async def test_get_expense_by_id_success(self, client, auth_headers, test_expense):
        response = await client.get(
            f"/expense/{test_expense.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_expense.id)
        assert data["description"] == test_expense.description
        assert Decimal(data["amount"]) == test_expense.amount
        assert "category" in data
        assert data["category"]["name"] == "Food"

    async def test_get_expense_by_id_not_found(self, client, auth_headers):
        fake_id = uuid4()
        response = await client.get(f"/expense/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    async def test_get_expense_by_id_invalid_uuid(self, client, auth_headers):
        response = await client.get("/expense/invalid-uuid", headers=auth_headers)
        assert response.status_code == 422

    async def test_get_expense_by_id_unauthorized(self, client, test_expense):
        response = await client.get(f"/expense/{test_expense.id}")
        assert response.status_code == 401


class TestGetExpenses:

    async def test_get_all_expenses(self, client, auth_headers, multiple_expenses):
        response = await client.get("/expense/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        assert isinstance(data, list)

    async def test_get_expenses_empty(self, client, auth_headers):
        response = await client.get("/expense/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_filter_by_category(self, client, auth_headers, multiple_expenses, predefined_categories):
        food_category_id = predefined_categories[0].id
        
        response = await client.get(
            f"/expense/?category_id={food_category_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(expense["category"]["id"] == str(food_category_id) for expense in data)

    async def test_filter_by_min_amount(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?min_amount=100",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(Decimal(expense["amount"]) >= Decimal("100.00") for expense in data)

    async def test_filter_by_max_amount(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?max_amount=50",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(Decimal(expense["amount"]) <= Decimal("50.00") for expense in data)

    async def test_filter_by_amount_range(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?min_amount=25&max_amount=100",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(Decimal("25.00") <= Decimal(expense["amount"]) <= Decimal("100.00") for expense in data)

    async def test_filter_by_date_range(self, client, auth_headers, multiple_expenses):
        start_date = get_past_date(days=4)
        end_date = get_current_date()
 
        response = await client.get(
            f"/expense/?from={start_date}&to={end_date}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    async def test_sort_by_amount_asc(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?sort_by=amount&sort_order=asc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        amounts = [Decimal(expense["amount"]) for expense in data]
        assert amounts == sorted(amounts)

    async def test_sort_by_amount_desc(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?sort_by=amount&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        amounts = [Decimal(expense["amount"]) for expense in data]
        assert amounts == sorted(amounts, reverse=True)

    async def test_sort_by_date_desc(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?sort_by=expense_date&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        dates = [expense["expense_date"] for expense in data]
        assert dates == sorted(dates, reverse=True)

    async def test_limit_results(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            "/expense/?limit=2",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_combined_filters(self, client, auth_headers, multiple_expenses, predefined_categories):
        food_category_id = predefined_categories[0].id
        
        response = await client.get(
            f"/expense/?category_id={food_category_id}&min_amount=50&sort_by=amount&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(expense["category"]["id"] == str(food_category_id) for expense in data)
        assert all(Decimal(expense["amount"]) >= Decimal("50.00") for expense in data)

    async def test_get_expenses_unauthorized(self, client):
        response = await client.get("/expense/")
        assert response.status_code == 401

class TestCreateExpense:

    async def test_create_expense_success(self, client, auth_headers, predefined_categories, test_user, db_session):
        expense_amount = Decimal("125.50")
        initial_balance = test_user.balance
        expense_data = {
            "amount": float(expense_amount),
            "description": "Restaurant dinner",
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[0].id)
        }
        
        response = await client.post(
            "/expense/",
            json=expense_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert Decimal(data["amount"]) == Decimal("125.50")
        assert data["description"] == "Restaurant dinner"
        assert "id" in data
        assert "category" in data

        await db_session.refresh(test_user)
        expected_balance = initial_balance - expense_amount
        assert test_user.balance == expected_balance
        assert test_user.balance == Decimal("874.50")

    async def test_create_expense_missing_amount(self, client, auth_headers, predefined_categories):
        expense_data = {
            "description": "Test",
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[0].id)
        }
        
        response = await client.post("/expense/", json=expense_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_expense_missing_description(self, client, auth_headers, predefined_categories):
        expense_data = {
            "amount": 50.00,
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[0].id)
        }
        
        response = await client.post("/expense/", json=expense_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_expense_missing_category_id(self, client, auth_headers):
        expense_data = {
            "amount": 50.00,
            "description": "Test",
            "expense_date": get_current_date().isoformat()
        }
        
        response = await client.post("/expense/", json=expense_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_expense_negative_amount(self, client, auth_headers, predefined_categories):
        expense_data = {
            "amount": -50.00,
            "description": "Test",
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[0].id)
        }
        
        response = await client.post("/expense/", json=expense_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_expense_zero_amount(self, client, auth_headers, predefined_categories):
        expense_data = {
            "amount": 0.00,
            "description": "Test",
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[0].id)
        }
        
        response = await client.post("/expense/", json=expense_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_expense_unauthorized(self, client, predefined_categories):
        expense_data = {
            "amount": 50.00,
            "description": "Test",
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[0].id)
        }
        
        response = await client.post("/expense/", json=expense_data)
        assert response.status_code == 401

class TestUpdateExpense:

    async def test_update_expense_amount(self, client, auth_headers, test_expense, test_user, db_session):
        old_amount = test_expense.amount
        new_amount = Decimal("75.00")
        initial_balance = test_user.balance
        update_data = {"amount": 75.00}
        
        response = await client.patch(
            f"/expense/{test_expense.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert Decimal(data["amount"]) == Decimal("75.00")
        assert data["description"] == test_expense.description

        await db_session.refresh(test_user)
        expected_balance = initial_balance - (new_amount - old_amount)
        assert test_user.balance == expected_balance
        assert test_user.balance == Decimal("975.00")

    async def test_update_expense_description(self, client, auth_headers, test_expense):
        update_data = {"description": "Updated description"}
        
        response = await client.patch(
            f"/expense/{test_expense.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"
        assert Decimal(data["amount"]) == test_expense.amount

    async def test_update_expense_category(self, client, auth_headers, test_expense, predefined_categories):
        new_category_id = predefined_categories[1].id
        update_data = {"category_id": str(new_category_id)}
        
        response = await client.patch(
            f"/expense/{test_expense.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["category"]["id"] == str(new_category_id)

    async def test_update_expense_all_fields(self, client, auth_headers, test_expense, predefined_categories):
        update_data = {
            "amount": 99.99,
            "description": "Updated description",
            "expense_date": get_current_date().isoformat(),
            "category_id": str(predefined_categories[1].id)
        }
        
        response = await client.patch(
            f"/expense/{test_expense.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert Decimal(data["amount"]) == Decimal("99.99")
        assert data["description"] == "Updated description"

    async def test_update_expense_not_found(self, client, auth_headers):
        fake_id = uuid4()
        update_data = {"amount": 100.00}
        
        response = await client.patch(
            f"/expense/{fake_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404

    async def test_update_expense_negative_amount(self, client, auth_headers, test_expense):
        update_data = {"amount": -50.00}
        
        response = await client.patch(
            f"/expense/{test_expense.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422

    async def test_update_expense_unauthorized(self, client, test_expense):
        update_data = {"amount": 100.00}
        response = await client.patch(f"/expense/{test_expense.id}", json=update_data)
        assert response.status_code == 401


class TestDeleteExpense:

    async def test_delete_expense_success(self, client, predefined_categories, auth_headers, test_user, db_session):
        initial_balance = test_user.balance
        expense_amount = Decimal("100.00")

        create_response = await client.post(
            "/expense/",
            json={
                "amount": float(expense_amount),
                "description": "Original description",
                "expense_date": get_current_date().isoformat(),
                "category_id": str(predefined_categories[1].id)
            },
            headers=auth_headers
        )
        expense_id = create_response.json()["id"]
        
        await db_session.refresh(test_user)
        assert test_user.balance == Decimal("900.00")

        response = await client.delete(f"/expense/{expense_id}", headers=auth_headers)
        assert response.status_code == 204

        await db_session.refresh(test_user)
        assert test_user.balance == initial_balance
        assert test_user.balance == Decimal("1000.00")
        
        get_response = await client.get(f"/expense/{expense_id}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_expense_unauthorized(self, client, test_expense):
        response = await client.delete(f"/expense/{test_expense.id}")
        assert response.status_code == 401


class TestDeleteExpensePermanently:

    async def test_delete_permanently_success(self, client, predefined_categories, auth_headers, test_user, db_session):
        initial_balance = test_user.balance
        expense_amount = Decimal("100.00")

        create_response = await client.post(
            "/expense/",
            json={
                "amount": float(expense_amount),
                "description": "Original description",
                "expense_date": get_current_date().isoformat(),
                "category_id": str(predefined_categories[1].id)
            },
            headers=auth_headers
        )
        expense_id = create_response.json()["id"]
        
        await db_session.refresh(test_user)
        assert test_user.balance == Decimal("900.00")

        response = await client.delete(f"/expense/{expense_id}/permanent", headers=auth_headers)
        assert response.status_code == 204

        await db_session.refresh(test_user)
        assert test_user.balance == initial_balance
        assert test_user.balance == Decimal("1000.00")
        
        get_response = await client.get(f"/expense/{expense_id}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_permanently_unauthorized(self, client, test_expense):
        response = await client.delete(f"/expense/{test_expense.id}/permanent")
        assert response.status_code == 401