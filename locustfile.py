from locust import HttpUser, task, between

class GudliftPerformanceTest(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """Executed when a simulated user starts."""
        self.club_email = "john@simplylift.co"
        self.club_name = "Simply Lift"
        self.competition_name = "Spring Festival"

    @task(3)
    def test_load_index_and_points(self):
        """Simulate viewing home page and public points board."""
        self.client.get("/")
        self.client.get("/points")

    @task(3)
    def test_login_and_view_competitions(self):
        """Simulate login and fetching competitions list (must be < 5s)."""
        self.client.post("/showSummary", data={"email": self.club_email})

    @task(2)
    def test_booking_page(self):
        """Simulate loading the booking page for a competition."""
        self.client.get(f"/book/{self.competition_name}/{self.club_name}")

    @task(1)
    def test_purchase_places(self):
        """Simulate purchasing places / updating points (must be < 2s)."""
        self.client.post("/purchasePlaces", data={
            "club": self.club_name,
            "competition": self.competition_name,
            "places": "1"
        })
