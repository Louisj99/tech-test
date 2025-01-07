from flask.testing import FlaskClient

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
