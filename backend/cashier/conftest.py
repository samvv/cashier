from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session

from cashier.core import build_engine
from cashier.dependencies import get_session
from cashier.main import app
from cashier.models.products import Product


@pytest.fixture(name="session", autouse=True)
def session_fixture():
    engine = build_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client", autouse=True)
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="data", autouse=True)
def data_fixture(session: Session):
    products = [
        Product(
            name='Product Test 1',
            stock=5,
            price=Decimal(10),
            ean='2052552',
            image_path=None,
        ),
    ]
    for product in products:
        session.add(product)
        session.commit()
        session.refresh(product)
