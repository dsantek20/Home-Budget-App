import pytest
from db.entities.types.statistic_type import PeriodType
from utils.datetime_helpers import get_current_date

pytestmark = pytest.mark.asyncio


class TestGetExpenseSummary:
    
    async def test_get_expense_summary_all_time(self, client, auth_headers, multiple_expenses):
        response = await client.get("/statistics/expenses", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == "all_time"
        assert data["expense_count"] == 4
        assert data["total_spent"] == 1400.50
        assert abs(data["average_expense"] - 350.125) < 0.01
        assert len(data["categories"]) == 3 
        assert data["start_date"] is None
        assert data["end_date"] is not None
    
    async def test_expense_summary_category_breakdown(self, client, auth_headers, multiple_expenses):
        response = await client.get("/statistics/expenses", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        categories = {cat["category"]: cat for cat in data["categories"]}
        
        assert "Housing" in categories
        housing = categories["Housing"]
        assert housing["total"] == 1200.00
        assert housing["count"] == 1
        assert abs(housing["percentage"] - 85.68) < 0.1 
    
    async def test_get_expense_summary_month(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            f"/statistics/expenses?period={PeriodType.MONTH.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.MONTH.value
        assert "start_date" in data
        assert "end_date" in data
        assert data["start_date"] is not None
        assert isinstance(data["expense_count"], int)
        assert isinstance(data["total_spent"], float)
    
    async def test_get_expense_summary_week(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            f"/statistics/expenses?period={PeriodType.WEEK.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.WEEK.value
        assert "categories" in data
        assert isinstance(data["categories"], list)
    
    async def test_get_expense_summary_quarter(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            f"/statistics/expenses?period={PeriodType.QUARTER.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.QUARTER.value
        assert data["expense_count"] == 4
    
    async def test_get_expense_summary_year(self, client, auth_headers, multiple_expenses):
        response = await client.get(
            f"/statistics/expenses?period={PeriodType.YEAR.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.YEAR.value
        assert data["expense_count"] == 4
    
    async def test_expense_summary_category_breakdown(self, client, auth_headers, multiple_expenses):
        response = await client.get("/statistics/expenses", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["categories"]) > 0
        
        for category in data["categories"]:
            assert "category" in category
            assert "total" in category
            assert "count" in category
            assert "percentage" in category
            assert "average" in category
            assert "transactions" in category
            assert isinstance(category["transactions"], list)
            
            if len(category["transactions"]) > 0:
                transaction = category["transactions"][0]
                assert "id" in transaction
                assert "amount" in transaction
                assert "description" in transaction
                assert "date" in transaction
    
    async def test_expense_summary_empty(self, client, auth_headers):
        response = await client.get("/statistics/expenses", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["expense_count"] == 0
        assert data["total_spent"] == 0
        assert data["average_expense"] == 0
        assert len(data["categories"]) == 0
    
    async def test_expense_summary_sorting(self, client, auth_headers, multiple_expenses):
        response = await client.get("/statistics/expenses", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        categories = data["categories"]
        if len(categories) > 1:
            for i in range(len(categories) - 1):
                assert categories[i]["total"] >= categories[i + 1]["total"]
    
    async def test_expense_summary_unauthorized(self, client):
        response = await client.get("/statistics/expenses")
        assert response.status_code == 401


class TestGetIncomeSummary:
    
    async def test_get_income_summary_all_time(self, client, auth_headers, multiple_incomes):
        response = await client.get("/statistics/incomes", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == "all_time"
        assert data["income_count"] == 4
        assert data["total_income"] == 7700.00
        assert data["average_income"] == 1925.00
        assert len(data["categories"]) == 3 
        assert data["start_date"] is None
        assert data["end_date"] is not None
        

        categories = {cat["category"]: cat for cat in data["categories"]}
        
        assert "Salary" in categories
        salary = categories["Salary"]
        assert salary["total"] == 6000.00
        assert salary["count"] == 2
        assert abs(salary["percentage"] - 77.92) < 0.1 
        assert salary["average"] == 3000.00 
        assert len(salary["transactions"]) == 2
    
    async def test_get_income_summary_empty(self, client, auth_headers):
        response = await client.get("/statistics/incomes", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == "all_time"
        assert data["income_count"] == 0
        assert data["total_income"] == 0.0
        assert data["average_income"] == 0.0
        assert len(data["categories"]) == 0
    
    async def test_get_income_summary_month(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            f"/statistics/incomes?period={PeriodType.MONTH.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.MONTH.value
        assert "start_date" in data
        assert "end_date" in data
        assert data["start_date"] is not None
    
    async def test_get_income_summary_week(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            f"/statistics/incomes?period={PeriodType.WEEK.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.WEEK.value
        assert "categories" in data
    
    async def test_get_income_summary_quarter(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            f"/statistics/incomes?period={PeriodType.QUARTER.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.QUARTER.value
        assert data["income_count"] == 4
    
    async def test_get_income_summary_year(self, client, auth_headers, multiple_incomes):
        response = await client.get(
            f"/statistics/incomes?period={PeriodType.YEAR.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.YEAR.value
        assert data["income_count"] == 4
    
    async def test_income_summary_category_breakdown(self, client, auth_headers, multiple_incomes):
        response = await client.get("/statistics/incomes", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["categories"]) > 0
        
        for category in data["categories"]:
            assert "category" in category
            assert "total" in category
            assert "count" in category
            assert "percentage" in category
            assert "average" in category
            assert "transactions" in category
            
            if len(category["transactions"]) > 0:
                transaction = category["transactions"][0]
                assert "id" in transaction
                assert "amount" in transaction
                assert "description" in transaction
                assert "date" in transaction
    
    async def test_income_summary_empty(self, client, auth_headers):
        response = await client.get("/statistics/incomes", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["income_count"] == 0
        assert data["total_income"] == 0
        assert data["average_income"] == 0
        assert len(data["categories"]) == 0
    
    async def test_income_summary_unauthorized(self, client):
        response = await client.get("/statistics/incomes")
        assert response.status_code == 401


class TestGetFinancialOverview:
    
    async def test_get_financial_overview_all_time(self, client, auth_headers, multiple_expenses, multiple_incomes):
        response = await client.get("/statistics/overview", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == "all_time"
        assert "total_income" in data
        assert "total_expenses" in data
        assert "net_balance" in data
        assert "current_account_balance" in data
        assert data["start_date"] is None
        assert data["end_date"] is not None
    
    async def test_get_financial_overview_month(self, client, auth_headers, multiple_expenses, multiple_incomes):
        response = await client.get(
            f"/statistics/overview?period={PeriodType.MONTH.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == PeriodType.MONTH.value
        assert "start_date" in data
        assert "end_date" in data
        assert data["start_date"] is not None
    
    async def test_financial_overview_calculations(self, client, auth_headers, multiple_expenses, multiple_incomes):
        response = await client.get("/statistics/overview", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        expected_net = data["total_income"] - data["total_expenses"]
        assert abs(data["net_balance"] - expected_net) < 0.01  
    
    async def test_financial_overview_with_only_expenses(self, client, auth_headers, multiple_expenses):
        response = await client.get("/statistics/overview", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_expenses"] > 0
        assert data["total_income"] == 0
        assert data["net_balance"] < 0  
    
    async def test_financial_overview_with_only_incomes(self, client, auth_headers, multiple_incomes):
        response = await client.get("/statistics/overview", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_income"] > 0
        assert data["total_expenses"] == 0
        assert data["net_balance"] > 0 
    
    async def test_financial_overview_empty(self, client, auth_headers):
        response = await client.get("/statistics/overview", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_income"] == 0
        assert data["total_expenses"] == 0
        assert data["net_balance"] == 0
        assert "current_account_balance" in data
    
    async def test_financial_overview_week(self, client, auth_headers, multiple_expenses, multiple_incomes):
        response = await client.get(
            f"/statistics/overview?period={PeriodType.WEEK.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == PeriodType.WEEK.value
    
    async def test_financial_overview_quarter(self, client, auth_headers, multiple_expenses, multiple_incomes):
        response = await client.get(
            f"/statistics/overview?period={PeriodType.QUARTER.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == PeriodType.QUARTER.value
    
    async def test_financial_overview_year(self, client, auth_headers, multiple_expenses, multiple_incomes):
        response = await client.get(
            f"/statistics/overview?period={PeriodType.YEAR.value}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == PeriodType.YEAR.value
    
    async def test_financial_overview_unauthorized(self, client):
        response = await client.get("/statistics/overview")
        assert response.status_code == 401


class TestStatisticsPeriodFilters:
    
    async def test_all_periods_valid(self, client, auth_headers, multiple_expenses, multiple_incomes):
        periods = [PeriodType.WEEK.value, PeriodType.MONTH.value, PeriodType.QUARTER.value, PeriodType.YEAR.value]
        
        for period in periods:
            response = await client.get(
                f"/statistics/expenses?period={period}",
                headers=auth_headers
            )
            assert response.status_code == 200
            assert response.json()["period"] == period
            
            response = await client.get(
                f"/statistics/incomes?period={period}",
                headers=auth_headers
            )
            assert response.status_code == 200
            assert response.json()["period"] == period
            
            response = await client.get(
                f"/statistics/overview?period={period}",
                headers=auth_headers
            )
            assert response.status_code == 200
            assert response.json()["period"] == period
    
    async def test__expense_invalid_period(self, client, auth_headers):
        response = await client.get(
            "/statistics/expenses?period=invalid",
            headers=auth_headers
        )
        assert response.status_code == 422

    async def test_income_invalid_period(self, client, auth_headers):
        response = await client.get(
            "/statistics/incomes?period=invalid",
            headers=auth_headers
        )
        assert response.status_code == 422
    
    async def test_overview_invalid_period(self, client, auth_headers):
        response = await client.get(
            "/statistics/overview?period=invalid",
            headers=auth_headers
        )
        assert response.status_code == 422