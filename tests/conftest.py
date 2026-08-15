import pytest
import server


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    server.clubs = [{"name": "Test Club", "email": "test@test.com", "points": "15"}]
    server.competitions = [
        {
            "name": "Test Competition",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "25",
        }
    ]
    with server.app.test_client() as client:
        yield client
