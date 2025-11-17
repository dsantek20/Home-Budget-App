from decimal import Decimal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from db.entities.income_entities import Income
from db.entities.types.category_type import CategoryType
from db.entities.expense_entities import Expense
from utils.datetime_helpers import get_current_date, get_past_date
from uuid import uuid4
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio  
from app import app
from db.entities.category_entities import Category
from auth.users_auth import create_jwt_token
from db.entities.user_entities import User
from db.entities.base_model import Base
from db.database import get_session
from tests.test_database import TestingSessionLocal, override_get_session, test_engine


app.dependency_overrides[get_session] = override_get_session

@pytest_asyncio.fixture(scope="function")
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(setup_database):
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def test_user(db_session):
    user = User(
        id=uuid4(),
        email="domagojsantek70@gmail.com",
        username="Domagoj",
        password="hashed_password",
        first_name="Domagoj",
        last_name="Santek",
        balance=Decimal("1000.00"),
        categories=[]
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_token(test_user):
    return create_jwt_token(test_user.email)


@pytest_asyncio.fixture
async def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def predefined_categories(db_session):
    categories = [
        Category(
            id=uuid4(),
            name="Food",
            description="Food shopping and dining",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Transportation",
            description="Car, fuel, public transport",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Housing",
            description="Rent, utilities, maintenance",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Healthcare",
            description="Medical expenses, insurance",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Entertainment",
            description="Movies, games, hobbies",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Shopping",
            description="Clothing, electronics, gifts",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Education",
            description="Courses, books, tuition",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Bills",
            description="Phone, internet, subscriptions",
            is_predefined=True,
            category_type=CategoryType.EXPENSE.value,
            user_id=None
        ),
        
        Category(
            id=uuid4(),
            name="Salary",
            description="Monthly salary",
            is_predefined=True,
            category_type=CategoryType.INCOME.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Freelance",
            description="Freelance work income",
            is_predefined=True,
            category_type=CategoryType.INCOME.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Investments",
            description="Investment returns",
            is_predefined=True,
            category_type=CategoryType.INCOME.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Gifts",
            description="Money gifts received",
            is_predefined=True,
            category_type=CategoryType.INCOME.value,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Other Income",
            description="Other sources",
            is_predefined=True,
            category_type=CategoryType.INCOME.value,
            user_id=None
        ),
    ]
    
    db_session.add_all(categories)
    await db_session.commit()
    
    for category in categories:
        await db_session.refresh(category)
    
    return categories

@pytest_asyncio.fixture
async def expense_categories(predefined_categories):
    return [cat for cat in predefined_categories if cat.category_type == CategoryType.EXPENSE.value]


@pytest_asyncio.fixture
async def income_categories(predefined_categories):
    return [cat for cat in predefined_categories if cat.category_type == CategoryType.INCOME.value]

@pytest_asyncio.fixture
async def test_expense(db_session, test_user, predefined_categories):
    expense = Expense(
        id=uuid4(),
        user_id=test_user.id,
        category_id=predefined_categories[0].id,
        amount=Decimal("50.00"),
        description="Groceries shopping",
        expense_date=get_current_date()
    )
    db_session.add(expense)
    await db_session.commit()
    await db_session.refresh(expense)
    return expense


@pytest_asyncio.fixture
async def multiple_expenses(db_session, test_user, predefined_categories):
    expenses = [
        Expense(
            id=uuid4(),
            user_id=test_user.id,
            category_id=predefined_categories[0].id,
            amount=Decimal("25.50"),
            description="Breakfast",
            expense_date=get_past_date(days=5)
        ),
        Expense(
            id=uuid4(),
            user_id=test_user.id,
            category_id=predefined_categories[1].id,
            amount=Decimal("100.00"),
            description="Gas",
            expense_date=get_past_date(days=3)
        ),
        Expense(
            id=uuid4(),
            user_id=test_user.id,
            category_id=predefined_categories[0].id,
            amount=Decimal("75.00"),
            description="Dinner",
            expense_date=get_past_date(days=1)
        ),
        Expense(
            id=uuid4(),
            user_id=test_user.id,
            category_id=predefined_categories[2].id, 
            amount=Decimal("1200.00"),
            description="Rent",
            expense_date=get_current_date()
        ),
    ]
    
    db_session.add_all(expenses)
    await db_session.commit()
    
    for expense in expenses:
        await db_session.refresh(expense)
    
    return expenses

@pytest_asyncio.fixture
async def test_income(db_session, test_user, income_categories):
    income = Income(
        id=uuid4(),
        user_id=test_user.id,
        category_id=income_categories[0].id, 
        amount=Decimal("3000.00"),
        description="Monthly salary",
        income_date=get_current_date()
    )
    db_session.add(income)
    await db_session.commit()
    await db_session.refresh(income)
    return income


@pytest_asyncio.fixture
async def multiple_incomes(db_session, test_user, income_categories):
    incomes = [
        Income(
            id=uuid4(),
            user_id=test_user.id,
            category_id=income_categories[0].id,  
            amount=Decimal("3000.00"),
            description="Monthly salary",
            income_date=get_past_date(days=5)
        ),
        Income(
            id=uuid4(),
            user_id=test_user.id,
            category_id=income_categories[1].id,  
            amount=Decimal("500.00"),
            description="Freelance project",
            income_date=get_past_date(days=3)
        ),
        Income(
            id=uuid4(),
            user_id=test_user.id,
            category_id=income_categories[0].id,  
            amount=Decimal("3000.00"),
            description="Monthly salary",
            income_date=get_past_date(days=1)
        ),
        Income(
            id=uuid4(),
            user_id=test_user.id,
            category_id=income_categories[2].id,  
            amount=Decimal("1200.00"),
            description="Dividends",
            income_date=get_current_date()
        ),
    ]
    
    db_session.add_all(incomes)
    await db_session.commit()
    
    for income in incomes:
        await db_session.refresh(income)
    
    return incomes
