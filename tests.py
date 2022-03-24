import pytest
from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client
        
def test_budget_item_1_page(client):
    response = client.get('/budget_items/1/')
    assert b'mouse' in response.data
