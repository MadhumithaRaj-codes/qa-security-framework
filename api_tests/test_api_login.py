import requests

def test_login_api():

    response = requests.post("http://127.0.0.1:5000", data={
        "username": "admin",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "Login" in response.text