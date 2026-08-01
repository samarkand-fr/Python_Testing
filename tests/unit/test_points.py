import pytest

def test_points_board_status_code(client):
    response = client.get('/points')
    assert response.status_code == 200

def test_points_board_content(client):
    response = client.get('/points')
    assert b'Clubs Points Board' in response.data
    assert b'Test Club' in response.data
    assert b'15' in response.data # The points mocked in conftest
