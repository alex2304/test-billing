### Как запустить
Сервер:
```shell
 uvicorn main:app --reload
```

Тесты:
```shell
pytest tests.py
```

### Сущности

client_balance:
- id
- balance

transactions:
- sender_id
- receiver_id
- amount

### Запросы

1. GET /client/1
Response:
200 - {
    id: 1
    balance: 100
}
404 - клиент не найден

2. POST /client
Response:
{
    id: 1,
    balance: 0
}

3. POST /client/1/topup
Body: 
{
    amount: 100
}
Response: 
200 - {
id: 1
balance: 200
}
400 - amount меньше либо равен 0
404 - клиент не найден

4. POST /client/1/transfer
Body
{
    receiver_id: 2
    amount: 100
}
Response
200 - {
    id: 2
    amount: 100
}
400 - недостаточно средств / получатель не найден / нельзя отправить самому себе
404 - клиент не найден
