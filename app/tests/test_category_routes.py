from uuid import uuid4
import pytest
from db.entities.types.category_type import CategoryType

pytestmark = pytest.mark.asyncio 

class TestGetPredefinedCategories:

    async def test_get_all_predefined_categories_success(self, client, auth_headers, predefined_categories):
        response = await client.get(
            "/category/predefined",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 13  
        category_names = [cat["name"] for cat in data]
        assert "Food" in category_names
        assert "Transportation" in category_names
        assert "Housing" in category_names

        assert "Salary" in category_names
        assert "Freelance" in category_names
        assert "Investments" in category_names

    async def test_get_all_predefined_categories_unauthorized(self, client, auth_headers):
        response = await client.get("/category/predefined")
        assert response.status_code == 401

class TestGetPredefinedExpenseCategories:

    async def test_get_all_expense_predefined_categories_success(self, client, auth_headers, expense_categories):
        response = await client.get(
            "/category/predefined/expense",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 8 
        
        for cat in data:
            assert cat["category_type"] == CategoryType.EXPENSE.value
        
        category_names = [cat["name"] for cat in data]
        
        assert "Food" in category_names
        assert "Transportation" in category_names
        assert "Housing" in category_names
        assert "Healthcare" in category_names
        assert "Entertainment" in category_names
        
        assert "Salary" not in category_names
        assert "Freelance" not in category_names

    async def test_get_all_expense_predefined_categories_unauthorized(self, client, auth_headers):
        response = await client.get("/category/predefined/expense")
        assert response.status_code == 401

class TestGetPredefinedIncomeCategories:

    async def test_get_all_income_predefined_categories_success(self, client, auth_headers, income_categories):
        response = await client.get(
            "/category/predefined/income",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5 
        
        for cat in data:
            assert cat["category_type"] == CategoryType.INCOME.value
        
        category_names = [cat["name"] for cat in data]
        
        assert "Salary" in category_names
        assert "Freelance" in category_names
        assert "Investments" in category_names
        assert "Gifts" in category_names
        assert "Other Income" in category_names
        
        assert "Food" not in category_names
        assert "Transportation" not in category_names
        assert "Housing" not in category_names

    async def test_get_all_income_predefined_categories_unauthorized(self, client, auth_headers):
        response = await client.get("/category/predefined/income")
        assert response.status_code == 401

class TestGetUserCustomCategories:

    async def test_get_custom_categories_empty(self, client, auth_headers):
        response = await client.get("/category/custom", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_custom_categories_with_data(self, client, auth_headers):
        create_response = await client.post("/category/",
                json={
                    "name": "My Custom Expense",
                    "description": "Custom expense category",
                    "category_type": CategoryType.EXPENSE.value
                },
                headers=auth_headers
        )
        assert create_response.status_code == 200
            
        create_response2 = await client.post(
            "/category/",
            json={
                "name": "My Custom Income",
                "description": "Custom income category",
                "category_type": CategoryType.INCOME.value
            },
            headers=auth_headers
        )
        assert create_response2.status_code == 200
            
        response = await client.get("/category/custom", headers=auth_headers)
            
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(cat["name"] == "My Custom Expense" for cat in data)
        assert any(cat["name"] == "My Custom Income" for cat in data)    

    async def test_get_custom_categories_unauthorized(self, client):
        response = await client.get("/category/custom")
        assert response.status_code == 401

class TestGetUserCustomExpenseCategories:

    async def test_get_custom_expense_categories_empty(self, client, auth_headers):
        response = await client.get("/category/custom/expense", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_custom_expense_categories(self, client, auth_headers):
        await client.post(
            "/category/",
            json={
                "name": "Custom Expense",
                "description": "Test",
                "category_type": CategoryType.EXPENSE.value
            },
            headers=auth_headers
        )
        
        await client.post(
            "/category/",
            json={
                "name": "Custom Income",
                "description": "Test",
                "category_type": CategoryType.INCOME.value
            },
            headers=auth_headers
        )
        
        response = await client.get("/category/custom/expense", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Custom Expense"
        assert data[0]["category_type"] == CategoryType.EXPENSE.value

    async def test_get_custom_expense_categories_unauthorized(self, client):
        response = await client.get("/category/custom/expense")
        assert response.status_code == 401

class TestGetUserCustomIncomeCategories:

    async def test_get_custom_income_categories_empty(self, client, auth_headers):
        response = await client.get("/category/custom/income", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_custom_income_categories(self, client, auth_headers):

        await client.post(
            "/category/",
            json={
                "name": "Custom Expense",
                "description": "Test",
                "category_type": CategoryType.EXPENSE.value
            },
            headers=auth_headers
        )
        
        await client.post(
            "/category/",
            json={
                "name": "Custom Income",
                "description": "Test",
                "category_type": CategoryType.INCOME.value
            },
            headers=auth_headers
        )
        
        response = await client.get("/category/custom/income", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Custom Income"
        assert data[0]["category_type"] == CategoryType.INCOME.value

    async def test_get_custom_income_categories_unauthorized(self, client):
        response = await client.get("/category/custom/income")
        assert response.status_code == 401

class TestGetAllCategories:

    async def test_get_all_categories(self, client, auth_headers, predefined_categories):
        response = await client.get("/category/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 13  

    async def test_get_all_categories_includes_custom(self, client, auth_headers, predefined_categories):
        await client.post(
            "/category/",
            json={
                "name": "Custom Cat",
                "description": "Test",
                "category_type": CategoryType.EXPENSE.value
            },
            headers=auth_headers
        )
        
        response = await client.get("/category/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 14
        assert any(cat["name"] == "Custom Cat" for cat in data)

    async def test_get_all_categories_unauthorized(self, client):
        response = await client.get("/category/")
        assert response.status_code == 401

class TestGetAllExpenseCategories:

    async def test_get_all_categories(self, client, auth_headers, predefined_categories):
        response = await client.get("/category/expense", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 8  

    async def test_get_expense_categories_all(self, client, auth_headers, predefined_categories):
        await client.post(
            "/category/",
            json={
                "name": "Custom Expense",
                "description": "Test",
                "category_type": CategoryType.EXPENSE.value
            },
            headers=auth_headers
        )
        
        response = await client.get("/category/expense", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9 
        
        for cat in data:
            assert cat["category_type"] == CategoryType.EXPENSE.value

class TestGetAllIncomeCategories:

    async def test_get_all_categories(self, client, auth_headers, predefined_categories):
        response = await client.get("/category/income", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 5  

    async def test_get_income_categories_all(self, client, auth_headers, predefined_categories):
        await client.post(
            "/category/",
            json={
                "name": "Custom Income",
                "description": "Test",
                "category_type": CategoryType.INCOME.value
            },
            headers=auth_headers
        )
        
        response = await client.get("/category/income", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 6 
        
        for cat in data:
            assert cat["category_type"] == CategoryType.INCOME.value

    async def test_get_all_categories_unauthorized(self, client):
        response = await client.get("/category/income")
        assert response.status_code == 401

class TestGetCategoryById:

    async def test_get_category_by_id_success(self, client, auth_headers, predefined_categories):
        category_id = predefined_categories[0].id
        
        response = await client.get(f"/category/{category_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(category_id)
        assert data["name"] == predefined_categories[0].name
        assert data["description"] == predefined_categories[0].description

    async def test_get_category_by_id_not_found(self, client, auth_headers):
        fake_id = uuid4()
        response = await client.get(f"/category/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    async def test_get_category_by_id_invalid_uuid(self, client, auth_headers):
        response = await client.get("/category/123546-4848-5485", headers=auth_headers)
        assert response.status_code == 422

    async def test_get_category_by_id_unauthorized(self, client, predefined_categories):
        category_id = predefined_categories[0].id
        response = await client.get(f"/category/{category_id}")
        assert response.status_code == 401

class TestCreateCustomCategory:

    async def test_create_expense_category_success(self, client, auth_headers):
        category_data = {
            "name": "Savings",
            "description": "Emergency fund and investments",
            "category_type": CategoryType.EXPENSE.value
        }
        
        response = await client.post(
            "/category/",
            json=category_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Savings"
        assert data["description"] == "Emergency fund and investments"
        assert data["category_type"] == CategoryType.EXPENSE.value
        assert "id" in data
    
    async def test_create_income_category_success(self, client, auth_headers):
        category_data = {
            "name": "Side Hustle",
            "description": "Extra income",
            "category_type": CategoryType.INCOME.value
        }
        
        response = await client.post(
            "/category/",
            json=category_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Side Hustle"
        assert data["category_type"] == CategoryType.INCOME.value

    async def test_create_category_missing_name(self, client, auth_headers):
        category_data = {
            "description": "Only description",
            "category_type": CategoryType.EXPENSE.value
        }
        
        response = await client.post("/category/", json=category_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_category_missing_description(self, client, auth_headers):
        category_data = {
            "name": "Only Name",
            "category_type": CategoryType.EXPENSE.value
        }
        
        response = await client.post("/category/", json=category_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_category_missing_type(self, client, auth_headers):
        category_data = {
            "name": "Test",
            "description": "Test"
        }
        
        response = await client.post("/category/", json=category_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_category_invalid_type(self, client, auth_headers):
        category_data = {
            "name": "Test",
            "description": "Test",
            "category_type": "INVALID"
        }
        
        response = await client.post("/category/", json=category_data, headers=auth_headers)
        assert response.status_code == 422

    async def test_create_category_unauthorized(self, client):
        category_data = {
            "name": "Savings",
            "description": "Test",
            "category_type": CategoryType.EXPENSE.value
        }
        
        response = await client.post("/category/", json=category_data)
        assert response.status_code == 401
    
class TestUpdateCategory:

    async def test_update_category_name(self, client, auth_headers):
        create_response = await client.post(
            "/category/",
            json={"name": "Original name", "description": "Original description", "category_type": CategoryType.EXPENSE.value},
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        update_data = {"name": "Updated Name"}
        response = await client.patch(
            f"/category/{category_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Original description"
        assert data["category_type"] == CategoryType.EXPENSE.value

    async def test_update_category_description(self, client, auth_headers):
        create_response = await client.post(
            "/category/",
            json={"name": "Original name", "description": "Original description", "category_type": CategoryType.EXPENSE.value},
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        update_data = {"description": "Updated description"}
        response = await client.patch(
            f"/category/{category_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Original name"  
        assert data["description"] == "Updated description"
        assert data["category_type"] == CategoryType.EXPENSE.value
    
    async def test_update_category_type(self, client, auth_headers):
        create_response = await client.post(
            "/category/",
            json={
                "name": "Test",
                "description": "Test",
                "category_type": CategoryType.EXPENSE.value
            },
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        update_data = {"category_type": CategoryType.INCOME.value}
        response = await client.patch(
            f"/category/{category_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["category_type"] == CategoryType.INCOME.value

    async def test_update_category_all_fields(self, client, auth_headers):
        create_response = await client.post(
            "/category/",
            json={"name": "Original name", "description": "Original description", "category_type": CategoryType.EXPENSE.value},
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        update_data = {
            "name": "Updated name",
            "description": "Updated description",
            "category_type": CategoryType.INCOME.value
        }
        response = await client.patch(
            f"/category/{category_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated name"
        assert data["description"] == "Updated description"
        assert data["category_type"] == CategoryType.INCOME.value

    async def test_update_category_not_found(self, client, auth_headers):
        fake_id = uuid4()
        update_data = {"name": "Updated"}
        
        response = await client.patch(
            f"/category/{fake_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404

    async def test_update_category_unauthorized(self, client, predefined_categories):
        category_id = predefined_categories[0].id
        response = await client.patch(f"/category/{category_id}", json={"name": "Updated name"})
        assert response.status_code == 401


class TestDeleteCategory:

    async def test_delete_category_success(self, client, auth_headers):
        create_response = await client.post(
            "/category/",
            json={"name": "Original name", "description": "Original description", "category_type": CategoryType.EXPENSE.value},
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        response = await client.delete(f"/category/{category_id}", headers=auth_headers)
        assert response.status_code == 204

        get_response = await client.get(f"/category/{category_id}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_category_unauthorized(self, client, predefined_categories):
        category_id = predefined_categories[0].id
        response = await client.delete(f"/category/{category_id}")
        assert response.status_code == 401


class TestDeleteCategoryPermanently:

    async def test_delete_permanently_success(self, client, auth_headers):
        create_response = await client.post(
            "/category/",
            json={"name": "Original name", "description": "Original description", "category_type": CategoryType.EXPENSE.value},
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        response = await client.delete(f"/category/{category_id}/permanent", headers=auth_headers)
        assert response.status_code == 204

        get_response = await client.get(f"/category/{category_id}", headers=auth_headers)
        assert get_response.status_code == 404

    async def test_delete_permanently_unauthorized(self, client, predefined_categories):
        category_id = predefined_categories[0].id
        response = await client.delete(f"/category/{category_id}/permanent")
        assert response.status_code == 401