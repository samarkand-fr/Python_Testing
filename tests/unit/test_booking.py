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

def test_issue_6_points_updates_are_reflected(client):
    # This test proves that Issue #6 is fixed: when a booking is confirmed,
    # the points are deducted and reflected correctly in the UI.
    
    # 1. Login
    response = client.post('/showSummary', data={'email': 'test@test.com'})
    assert b'Points available: 15' in response.data
    
    # 2. Book 5 places
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5'
    })
    
    # 3. Check the UI again, points should be 10 now
    assert b'Points available: 10' in response.data

def test_purchase_places_more_than_available(client):
    club = [c for c in server.clubs if c['name'] == 'Test Club'][0]
    club['points'] = 50
    competition = [c for c in server.competitions if c['name'] == 'Test Competition'][0]
    competition['numberOfPlaces'] = 5
    
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '10' # More than 5 available
    })
    
    assert response.status_code == 200
    assert b'There are not enough places available in this competition.' in response.data
    assert int(competition['numberOfPlaces']) == 5

def test_purchase_places_zero_or_negative(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '-5'
    })
    
    assert response.status_code == 200
    assert b'You must book at least 1 place.' in response.data
