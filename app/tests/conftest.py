import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
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
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Transportation",
            description="Car, fuel, public transport",
            is_predefined=True,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Housing",
            description="Rent, utilities, maintenance",
            is_predefined=True,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Healthcare",
            description="Medical expenses, insurance",
            is_predefined=True,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Entertainment",
            description="Movies, games, hobbies",
            is_predefined=True,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Shopping",
            description="Clothing, electronics, gifts",
            is_predefined=True,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Education",
            description="Courses, books, tuition",
            is_predefined=True,
            user_id=None
        ),
        Category(
            id=uuid4(),
            name="Bills",
            description="Phone, internet, subscriptions",
            is_predefined=True,
            user_id=None
        ),
    ]
    
    db_session.add_all(categories)
    await db_session.commit()
    
    for category in categories:
        await db_session.refresh(category)
    
    return categories
