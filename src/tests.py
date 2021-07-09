from unittest.mock import patch

from fastapi.testclient import TestClient

from errors import ReceiverNotFound, InsufficientBalance
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


# === GET /client/{client_id} ===


@patch("logic.get_client_by_id")
def test_get_client(get_client_mock):
    get_client_mock.return_value = ClientData(id=1, balance=0.0)

    response = client.get("/client/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "balance": 0.0}

    get_client_mock.assert_called_once_with(1)


@patch("logic.get_client_by_id")
def test_get_client_404(get_client_mock):
    get_client_mock.return_value = None

    response = client.get("/client/100")
    assert response.status_code == 404

    get_client_mock.assert_called_once_with(100)


# === POST /client/{client_id}/topup ===


@patch("logic.top_up_client_balance")
def test_top_up_client_balance(top_up_client_balance_mock):
    amount = 50.5
    top_up_client_balance_mock.return_value = ClientData(id=1, balance=amount)

    response = client.post("/client/1/topup", json={"amount": amount})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "balance": amount}

    top_up_client_balance_mock.assert_called_once_with(1, amount=amount)


@patch("logic.top_up_client_balance")
def test_top_up_client_balance_422(top_up_client_balance_mock, subtests):
    for amount, expected_message in (
        ("a", "value is not a valid float"),
        (-1, "amount must be greater than 0"),
        (0, "amount must be greater than 0"),
    ):
        with subtests.test(msg=f"amount={amount}"):
            response = client.post("/client/1/topup", json={"amount": amount})
            assert response.status_code == 422, response.text
            assert response.json()["detail"][0]["msg"] == expected_message, response.json()

    top_up_client_balance_mock.assert_not_called()


@patch("logic.top_up_client_balance")
def test_top_up_client_balance_404(top_up_client_balance_mock):
    top_up_client_balance_mock.return_value = None

    response = client.post("/client/1/topup", json={"amount": 1})
    assert response.status_code == 404, response.text

    top_up_client_balance_mock.assert_called_once_with(1, amount=1)


# === POST /client/{client_id}/transfer ===


@patch("logic.transfer_money")
def test_transfer_money(transfer_money_mock):
    amount = 50.5
    transfer_money_mock.return_value = ClientData(id=1, balance=0)

    response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": amount})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "balance": 0}

    transfer_money_mock.assert_called_once_with(1, receiver_id=2, amount=amount)


@patch("logic.transfer_money")
def test_transfer_money_404(transfer_money_mock):
    transfer_money_mock.return_value = None

    response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": 1})
    assert response.status_code == 404, response.text

    transfer_money_mock.assert_called_once_with(1, receiver_id=2, amount=1)


@patch("logic.transfer_money")
def test_transfer_money_422_wrong_amount(transfer_money_mock, subtests):
    for amount, expected_message in (
        ("a", "value is not a valid float"),
        (-1, "amount must be greater than 0"),
        (0, "amount must be greater than 0"),
    ):
        with subtests.test(msg=f"amount={amount}"):
            response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": amount})
            assert response.status_code == 422, response.text
            assert response.json()["detail"][0]["msg"] == expected_message, response.json()

    transfer_money_mock.assert_not_called()


@patch("logic.transfer_money")
def test_transfer_money_422_same_sender_receiver(transfer_money_mock):
    response = client.post("/client/1/transfer", json={"receiver_id": 1, "amount": 1})
    assert response.status_code == 422, response.text
    assert response.json()["detail"] == "Sender and receiver must be different", response.json()

    transfer_money_mock.assert_not_called()


@patch("logic.transfer_money")
def test_transfer_money_422_receiver_not_found(transfer_money_mock):
    transfer_money_mock.side_effect = ReceiverNotFound

    response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": 1})
    assert response.status_code == 422, response.text
    assert response.json()["detail"] == "No receiver with such id", response.json()

    transfer_money_mock.assert_called_once_with(1, receiver_id=2, amount=1)


@patch("logic.transfer_money")
def test_transfer_money_422_insufficient_balance(transfer_money_mock):
    transfer_money_mock.side_effect = InsufficientBalance

    response = client.post("/client/1/transfer", json={"receiver_id": 2, "amount": 1})
    assert response.status_code == 422, response.text
    assert response.json()["detail"] == "Sender doesn't have enough balance", response.json()

    transfer_money_mock.assert_called_once_with(1, receiver_id=2, amount=1)
