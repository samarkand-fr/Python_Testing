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
    club['points'] = 2
    
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5' # More than 2 points, but less than 12
    })
    assert response.status_code == 200
    assert b'You do not have enough points' in response.data
    # Points should not be deducted
    assert int(club['points']) == 2

def test_purchase_places_more_than_12(client):
    # Club has enough points (15) and competition has enough places (25)
    club = [c for c in server.clubs if c['name'] == 'Test Club'][0]
    club['points'] = 15
    
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '13' # More than 12
    })
    assert response.status_code == 200
    assert b'You cannot book more than 12 places' in response.data
    # Points should not be deducted
    assert int(club['points']) == 15

def test_purchase_places_past_competition(client):
    server.competitions.append({
        "name": "Past Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"
    })
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Past Competition',
        'places': '5'
    })
    assert response.status_code == 200
    assert b'You cannot book places for a past competition.' in response.data
