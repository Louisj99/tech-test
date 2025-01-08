from flask.testing import FlaskClient

# my method for tests is to test everywhere there can be a failure normally this is anywhere
#there is error handling, a return statement, or a conditional statement.
# for this case I ended up testing the entire file because of the way I split it up everything pretty much had a return or a conditional statement
# I also tested the default case to make sure that the normal case was working as expected

# the following is the coverage report for the project file
# Name                          Stmts   Miss  Cover   Missing
# -----------------------------------------------------------
# __init__.py                       0      0   100%
# tests/api_test.py                54      0   100%
# tests/conftest.py                13      0   100%
# user_monitoring/__init__.py       0      0   100%
# user_monitoring/api.py           71      0   100%
# user_monitoring/app.py            9      1    89%   15
# -----------------------------------------------------------
# TOTAL                           147      1    99%

# to get the coverage I used pytest (the testing framework) and pytest-cov (the coverage plugin)




#default test no alert codes
def test_handle_user_event(client: FlaskClient) -> None:
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "42.00",
        "user_id": 1,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 1}

def test_handle_user_event_invalid_media_type(client: FlaskClient) -> None:
    response = client.post("/event")
    assert response.status_code == 415

def test_handle_user_event_invalid_json(client: FlaskClient) -> None:
    response = client.post("/event", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid JSON data", "status_code": 400}

def test_handle_invalid_media_type(client: FlaskClient) -> None:
    response = client.post("/event", data="{}")
    assert response.status_code == 415
    assert response.json == {"error": "Invalid media type", "status_code": 415}

def test_handle_missing_key(client: FlaskClient) -> None:
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "42.00",
        "time": 10
    })
    assert response.status_code == 400
    assert response.json == {"error": "Missing key: 'user_id'", "status_code": 400}

def test_handle_withdrawal_limit(client: FlaskClient) -> None:
    response = client.post("/event", json={
        "type": "withdrawal",
        "amount": "110.00",
        "user_id": 1,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json == {'alert': True, 'alert_codes': [1100], 'user_id': 1}

def test_handle_consecutive_withdrawals(client: FlaskClient) -> None:
    response = client.post("/event", json={
        "type": "withdrawal",
        "amount": "50.00",
        "user_id": 2,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 2}
    response = client.post("/event", json={
        "type": "withdrawal",
        "amount": "60.00",
        "user_id": 2,
        "time": 20
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 2}
    response = client.post("/event", json={
        "type": "withdrawal",
        "amount": "70.00",
        "user_id": 2,
        "time": 30
    })
    assert response.status_code == 200
    assert response.json == {'alert': True, 'alert_codes': [30], 'user_id': 2}

def test_handle_consecutive_large_deposits(client: FlaskClient) -> None:
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "10.00",
        "user_id": 3,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 3}
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "20.00",
        "user_id": 3,
        "time": 20
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 3}
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "30.00",
        "user_id": 3,
        "time": 30
    })
    assert response.status_code == 200
    assert response.json == {'alert': True, 'alert_codes': [300], 'user_id': 3}

def test_handle_total_deposits_in_window(client: FlaskClient) -> None:
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "100.00",
        "user_id": 4,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 4}
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "100.00",
        "user_id": 4,
        "time": 20
    })
    assert response.status_code == 200
    assert response.json == {'alert': False, 'alert_codes': [], 'user_id': 4}
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "100.00",
        "user_id": 4,
        "time": 30
    })
    assert response.status_code == 200
    assert response.json == {'alert': True, 'alert_codes': [123], 'user_id': 4}