from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_client():
    response = client.post("/client/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "balance": 0.0}


def test_get_client():
    response = client.get("/client/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "balance": 0.0}


def test_top_up_client_balance():
    response = client.post("/client/1/topup", json={"amount": 50.5})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "balance": 150.5}


def test_transfer_money():
    response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": 50.5})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "balance": 49.5}
