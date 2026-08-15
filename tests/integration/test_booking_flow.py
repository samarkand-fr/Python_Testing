import pytest
import server


def test_full_successful_booking_workflow(client):
    """
    Integration Test: Complete user workflow.
    1. Log in with a valid email.
    2. Access booking page for a valid competition.
    3. Purchase valid number of places.
    4. Confirm points & places deduction.
    5. Confirm points updated on public points board.
    6. Log out.
    """
    # 1. Login
    login_res = client.post("/showSummary", data={"email": "test@test.com"})
    assert login_res.status_code == 200
    assert b"Welcome, test@test.com" in login_res.data
    assert b"Points available: 15" in login_res.data

    # 2. Get booking page
    book_page_res = client.get("/book/Test Competition/Test Club")
    assert book_page_res.status_code == 200
    assert b"Booking for Test Competition" in book_page_res.data

    # 3. Purchase 4 places
    purchase_res = client.post(
        "/purchasePlaces",
        data={"club": "Test Club", "competition": "Test Competition", "places": "4"},
    )
    assert purchase_res.status_code == 200
    assert b"Great-booking complete!" in purchase_res.data
    assert b"Points available: 11" in purchase_res.data

    # 4. Check public points board reflects deduction
    points_res = client.get("/points")
    assert points_res.status_code == 200
    assert b"Test Club" in points_res.data
    assert b"11" in points_res.data

    # 5. Logout
    logout_res = client.get("/logout", follow_redirects=True)
    assert logout_res.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in logout_res.data


def test_failed_booking_workflow_keeps_state_intact(client):
    """
    Integration Test: Failed booking attempt due to exceeding limits.
    Ensures state (points, places) is not modified when validation fails.
    """
    # 1. Attempt invalid booking (requesting 13 places - exceeds 12 limit)
    purchase_res = client.post(
        "/purchasePlaces",
        data={"club": "Test Club", "competition": "Test Competition", "places": "13"},
    )
    assert purchase_res.status_code == 200
    assert (
        b"You cannot book more than 12 places in a single competition."
        in purchase_res.data
    )
    assert b"Points available: 15" in purchase_res.data

    # 2. Verify competition places remain unchanged (25)
    comp = [c for c in server.competitions if c["name"] == "Test Competition"][0]
    assert int(comp["numberOfPlaces"]) == 25

    # 3. Verify club points remain unchanged (15)
    club = [c for c in server.clubs if c["name"] == "Test Club"][0]
    assert int(club["points"]) == 15


def test_multiple_consecutive_bookings_accumulate_deductions(client):
    """
    Integration Test: Consecutive bookings by the same club.
    Ensures deductions accumulate properly across multiple transactions.
    """
    # First booking: 3 places (15 - 3 = 12 points)
    res1 = client.post(
        "/purchasePlaces",
        data={"club": "Test Club", "competition": "Test Competition", "places": "3"},
    )
    assert res1.status_code == 200
    assert b"Points available: 12" in res1.data

    # Second booking: 5 places (12 - 5 = 7 points)
    res2 = client.post(
        "/purchasePlaces",
        data={"club": "Test Club", "competition": "Test Competition", "places": "5"},
    )
    assert res2.status_code == 200
    assert b"Points available: 7" in res2.data

    # Verify final remaining competition places (25 - 3 - 5 = 17)
    comp = [c for c in server.competitions if c["name"] == "Test Competition"][0]
    assert int(comp["numberOfPlaces"]) == 17
