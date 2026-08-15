import pytest


def test_login_valid_email(client):
    response = client.post("/showSummary", data={"email": "test@test.com"})
    assert response.status_code == 200
    assert b"Welcome, test@test.com" in response.data


def test_login_invalid_email(client):
    response = client.post("/showSummary", data={"email": "unknown@test.com"})
    # Right now, this throws an IndexError in the app.
    # When fixed, it should redirect (302) or return 200 with an error message in flash.
    # The requirement says we should show an error message
    # and we should be redirected or stay at index.
    # Looking at similar flask patterns, typically they redirect back to index,
    # or render index with error.
    # Let's say it redirects to index.
    assert response.status_code == 302
