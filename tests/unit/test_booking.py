import pytest
import server

def test_purchase_places_valid(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5'
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    # Points should be deducted (15 - 5 = 10)
    club = [c for c in server.clubs if c['name'] == 'Test Club'][0]
    assert int(club['points']) == 10

def test_purchase_places_more_than_points(client):
    # Reset points for the test
    club = [c for c in server.clubs if c['name'] == 'Test Club'][0]
    club['points'] = 15
    
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '20' # More than 15 points
    })
    assert response.status_code == 200
    assert b'You do not have enough points' in response.data
    # Points should not be deducted
    assert int(club['points']) == 15
