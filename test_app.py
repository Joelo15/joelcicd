from app import app

def test_suma_endpoint():
    client = app.test_client()
    response = client.get("/suma?a=3&b=5")
    data = response.get_json()
    assert response.status_code == 200
    assert data["resultado"] == 8
