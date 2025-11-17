from decimal import Decimal
from uuid import uuid4
import pytest
from utils.datetime_helpers import get_current_date, get_past_date

pytestmark = pytest.mark.asyncio 


class TestGetIncomeById:

    async def test_get_income_by_id_success(self, client, auth_headers, test_income):
        response = await client.get(
            f"/income/{test_income.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_income.id)
        assert data["description"] == test_income.description
        assert Decimal(data["amount"]) == test_income.amount
        assert "category" in data
        assert data["category"]["name"] == "Salary"

    async def test_get_income_by_id_not_found(self, client, auth_headers):
        fake_id = uuid4()
        response = await client.get(f"/income/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    async def test_get_income_by_id_invalid_uuid(self, client, auth_headers):
        response = await client.get("/income/invalid-uuid", headers=auth_headers)
        assert response.status_code == 422

    async def test_get_income_by_id_unauthorized(self, client, test_income):
        response = await client.get(f"/income/{test_income.id}")
        assert response.status_code == 401


class TestGetIncomes:

    async def test_get_all_incomes(self, client, auth_headers, multiple_incomes):
        response = await client.get("/income/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        assert isinstance(data, list)

    async def test_get_incomes_empty(self, client, auth_headers):
        response = await client.get("/income/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_filter_by_category(self, client, auth_headers, multiple_incomes, income_categories):
        salary_category_id = income_categories[0].id 
        
        response = await client.get(
            f"/income/?category_id={salary_category_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(income["category"]["id"] == str(salary_category_id) for income in data)

    async def test_filter_by_min_amount(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?min_amount=1000",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(Decimal(income["amount"]) >= Decimal("1000.00") for income in data)

    async def test_filter_by_max_amount(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?max_amount=500",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(Decimal(income["amount"]) <= Decimal("500.00") for income in data)

    async def test_filter_by_amount_range(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?min_amount=500&max_amount=3000",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(Decimal("500.00") <= Decimal(income["amount"]) <= Decimal("3000.00") for income in data)

    async def test_filter_by_date_range(self, client, auth_headers, multiple_incomes):
        start_date = get_past_date(days=4)
        end_date = get_current_date()
 
        response = await client.get(
            f"/income/?from={start_date}&to={end_date}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    async def test_sort_by_amount_asc(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?sort_by=amount&sort_order=asc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        amounts = [Decimal(income["amount"]) for income in data]
        assert amounts == sorted(amounts)

    async def test_sort_by_amount_desc(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?sort_by=amount&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        amounts = [Decimal(income["amount"]) for income in data]
        assert amounts == sorted(amounts, reverse=True)

    async def test_sort_by_date_desc(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?sort_by=income_date&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        dates = [income["income_date"] for income in data]
        assert dates == sorted(dates, reverse=True)

    async def test_limit_results(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            "/income/?limit=2",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_combined_filters(self, client, auth_headers, multiple_incomes, income_categories):
        salary_category_id = income_categories[0].id
        
        response = await client.get(
            f"/income/?category_id={salary_category_id}&min_amount=1000&sort_by=amount&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(income["category"]["id"] == str(salary_category_id) for income in data)
        assert all(Decimal(income["amount"]) >= Decimal("1000.00") for income in data)

    async def test_get_incomes_unauthorized(self, client):
        response = await client.get("/income/")
        assert response.status_code == 401


class TestCreateIncome:

    async def test_create_income_success(self, client, auth_headers, income_categories, test_user, db_session):
        income_amount = Decimal("3000.00")
        initial_balance = test_user.balance
        
        income_data = {
            "amount": float(income_amount),
            "description": "Monthly salary",
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[0].id) 
        }
        
        response = await client.post(
            "/income/",
            json=income_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert Decimal(data["amount"]) == income_amount
        assert data["description"] == "Monthly salary"
        assert "id" in data
        assert "category" in data
        
        await db_session.refresh(test_user)
        expected_balance = initial_balance + income_amount
        assert test_user.balance == expected_balance
        assert test_user.balance == Decimal("4000.00")

    async def test_create_income_with_expense_category(self, client, auth_headers, expense_categories):
        income_data = {
            "amount": 1000.00,
            "description": "Test",
            "income_date": get_current_date().isoformat(),
            "category_id": str(expense_categories[0].id) 
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 400

    async def test_create_income_missing_amount(self, client, auth_headers, income_categories):
        income_data = {
            "description": "Test",
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[0].id)
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_income_missing_description(self, client, auth_headers, income_categories):
        income_data = {
            "amount": 1000.00,
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[0].id)
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_income_missing_category_id(self, client, auth_headers):
        income_data = {
            "amount": 1000.00,
            "description": "Test",
            "income_date": get_current_date().isoformat()
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_income_negative_amount(self, client, auth_headers, income_categories):
        income_data = {
            "amount": -1000.00,
            "description": "Test",
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[0].id)
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_income_zero_amount(self, client, auth_headers, income_categories):
        income_data = {
            "amount": 0.00,
            "description": "Test",
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[0].id)
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_income_invalid_category(self, client, auth_headers):
        income_data = {
            "amount": 1000.00,
            "description": "Test",
            "income_date": get_current_date().isoformat(),
            "category_id": str(uuid4())
        }
        
        response = await client.post("/income/", json=income_data, headers=auth_headers)
        assert response.status_code == 404

    async def test_create_income_unauthorized(self, client, income_categories):
        income_data = {
            "amount": 1000.00,
            "description": "Test",
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[0].id)
        }
        
        response = await client.post("/income/", json=income_data)
        assert response.status_code == 401


class TestUpdateIncome:

    async def test_update_income_amount(self, client, auth_headers, test_income, test_user, db_session):
        old_amount = test_income.amount
        new_amount = Decimal("3500.00")
        initial_balance = test_user.balance
        
        update_data = {"amount": float(new_amount)}
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert Decimal(data["amount"]) == new_amount
        assert data["description"] == test_income.description
        
        await db_session.refresh(test_user)

        expected_balance = initial_balance + (new_amount - old_amount)
        assert test_user.balance == expected_balance

    async def test_update_income_amount_decrease(self, client, auth_headers, test_income, test_user, db_session):
        old_amount = test_income.amount
        new_amount = Decimal("2500.00")
        initial_balance = test_user.balance
        
        update_data = {"amount": float(new_amount)}
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        
        await db_session.refresh(test_user)

        expected_balance = initial_balance + (new_amount - old_amount)
        assert test_user.balance == expected_balance

    async def test_update_income_description(self, client, auth_headers, test_income, test_user, db_session):
        initial_balance = test_user.balance
        
        update_data = {"description": "Updated salary description"}
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated salary description"
        assert Decimal(data["amount"]) == test_income.amount
        
        await db_session.refresh(test_user)
        assert test_user.balance == initial_balance

    async def test_update_income_category(self, client, auth_headers, test_income, income_categories):
        new_category_id = income_categories[1].id  
        update_data = {"category_id": str(new_category_id)}
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["category"]["id"] == str(new_category_id)

    async def test_update_income_with_expense_category(self, client, auth_headers, test_income, expense_categories):
        update_data = {"category_id": str(expense_categories[0].id)}
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400

    async def test_update_income_all_fields(self, client, auth_headers, test_income, income_categories):
        update_data = {
            "amount": 4000.00,
            "description": "Updated description",
            "income_date": get_current_date().isoformat(),
            "category_id": str(income_categories[1].id)
        }
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert Decimal(data["amount"]) == Decimal("4000.00")
        assert data["description"] == "Updated description"

    async def test_update_income_not_found(self, client, auth_headers):
        fake_id = uuid4()
        update_data = {"amount": 1000.00}
        
        response = await client.patch(
            f"/income/{fake_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404

    async def test_update_income_negative_amount(self, client, auth_headers, test_income):
        update_data = {"amount": -1000.00}
        
        response = await client.patch(
            f"/income/{test_income.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422

    async def test_update_income_unauthorized(self, client, test_income):
        update_data = {"amount": 1000.00}
        response = await client.patch(f"/income/{test_income.id}", json=update_data)
        assert response.status_code == 401


class TestDeleteIncome:

    async def test_delete_income_success(self, client, income_categories, auth_headers, test_user, db_session):
        initial_balance = test_user.balance
        income_amount = Decimal("1000.00")
        
        create_response = await client.post(
            "/income/",
            json={
                "amount": float(income_amount),
                "description": "To delete",
                "income_date": get_current_date().isoformat(),
                "category_id": str(income_categories[0].id)
            },
            headers=auth_headers
        )
        income_id = create_response.json()["id"]
        
        await db_session.refresh(test_user)
        assert test_user.balance == Decimal("2000.00") 
        
        response = await client.delete(f"/income/{income_id}", headers=auth_headers)
        assert response.status_code == 204
        
        await db_session.refresh(test_user)
        assert test_user.balance == initial_balance
        assert test_user.balance == Decimal("1000.00")
        
        get_response = await client.get(f"/income/{income_id}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_income_unauthorized(self, client, test_income):
        """Test bez autorizacije"""
        response = await client.delete(f"/income/{test_income.id}")
        assert response.status_code == 401


class TestDeleteIncomePermanently:

    async def test_delete_permanently_success(self, client, income_categories, auth_headers, test_user, db_session):
        initial_balance = test_user.balance
        income_amount = Decimal("1000.00")
        
        create_response = await client.post(
            "/income/",
            json={
                "amount": float(income_amount),
                "description": "To delete",
                "income_date": get_current_date().isoformat(),
                "category_id": str(income_categories[0].id)
            },
            headers=auth_headers
        )
        income_id = create_response.json()["id"]
        
        await db_session.refresh(test_user)
        assert test_user.balance == Decimal("2000.00")
        
        response = await client.delete(f"/income/{income_id}/permanent", headers=auth_headers)
        assert response.status_code == 204
        
        await db_session.refresh(test_user)
        assert test_user.balance == initial_balance
        assert test_user.balance == Decimal("1000.00")
        
        get_response = await client.get(f"/income/{income_id}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_permanently_unauthorized(self, client, test_income):
        response = await client.delete(f"/income/{test_income.id}/permanent")
        assert response.status_code == 401