from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from models import ClientData

client = TestClient(app)


@patch("logic.create_client")
def test_create_client(create_client_mock):
    create_client_mock.return_value = ClientData(id=1, balance=0.0)

    response = client.post("/client/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "balance": 0.0}

    create_client_mock.assert_called_once_with()


@patch("logic.get_client_by_id")
def test_get_client(get_client_mock):
    get_client_mock.return_value = ClientData(id=1, balance=0.0)

    response = client.get("/client/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "balance": 0.0}

    get_client_mock.assert_called_once_with(1)


@patch("logic.top_up_client_balance")
def test_top_up_client_balance(top_up_client_balance_mock):
    amount = 50.5
    top_up_client_balance_mock.return_value = ClientData(id=1, balance=amount)

    response = client.post("/client/1/topup", json={"amount": amount})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "balance": amount}

    top_up_client_balance_mock.assert_called_once_with(1, amount=amount)


@patch("logic.transfer_money")
def test_transfer_money(transfer_money_mock):
    amount = 50.5
    transfer_money_mock.return_value = ClientData(id=1, balance=0)

    response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": amount})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "balance": 0}

    transfer_money_mock.assert_called_once_with(1, receiver_id=2, amount=amount)
