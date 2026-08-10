# GUDLFT Registration Portal

A lightweight proof-of-concept (POC) booking platform for local and regional powerlifting competition organizers. The application allows club secretaries to manage and redeem points to register athletes for upcoming competitions.

---

## 1. Project Overview & Features

- **Secretary Authentication**: Simple email-based login for authorized club secretaries.
- **Competition Booking**: Secretaries can redeem club points for competition places (1 point = 1 place).
- **Fairness Rules**:
  - Maximum **12 places** per competition per club.
  - Booking prohibited if points are insufficient.
  - Booking prohibited if competition places are sold out.
  - Booking prohibited for past competitions.
- **Public Points Board**: A public, read-only display (`/points`) showing the current point balance for all clubs without requiring login.

---

## 2. Fork & Repository Origin

This repository is a fork of the original OpenClassrooms project repository:
- **Upstream Repository**: [`OpenClassrooms-Student-Center/Python_Testing`](https://github.com/OpenClassrooms-Student-Center/Python_Testing)
- **Fork Repository**: [`samarkand-fr/Python_Testing`](https://github.com/samarkand-fr/Python_Testing)

All bug fixes, enhancements, and Phase 2 features were developed in isolated branches, thoroughly tested, and merged into `master`.

---

## 3. Issues & Branch Resolution Matrix

| Issue # | Description / Bug Summary | Dedicated Git Branch | Status | Solution Overview |
| :--- | :--- | :--- | :--- | :--- |
| **#1** | App 500 crash on unknown email login | `bug/login-email-crash` | ✅ Resolved | Added email validation in `/showSummary` with flash message error instead of raising `IndexError`. |
| **#2** | Points balance not deducted & over-redemption allowed | `bug/points-redemption` | ✅ Resolved | Added check against club available points in `/purchasePlaces` and deducted points from club balance upon confirmation. |
| **#4** | Booking more than 12 places allowed | `bug/12-places-limit` | ✅ Resolved | Enforced 12-place fairness limit in backend and set dynamic `max` attribute on booking form input. |
| **#5** | Booking allowed for past competitions | `bug/booking-past-competitions` | ✅ Resolved | Added `datetime` comparison in `/book` and `/purchasePlaces` to block booking past competitions. |
| **#6** | Updated points not reflected in UI dashboard | `bug/issue-6-point-updates` | ✅ Resolved | Re-rendered updated points balance on dashboard and added dedicated unit test proving UI state accuracy. |
| **#7** | Public points display board required (Phase 2) | `feature/points-board` | ✅ Resolved | Created public, read-only `/points` route and `points.html` view accessible without logging in. |
| **#282** | Booking more places than available in competition | `bug/issue-282-competition-places` | ✅ Resolved | Added check against competition remaining places and blocked negative/zero place inputs. |
| **N/A** | Integration & End-to-End Test Suite | `test/integration-booking-flow` | ✅ Resolved | Added 3 multi-step integration test flows in `tests/integration/` (Coverage: 94%). |
| **N/A** | Locust Performance Load Testing | `perf/locust-tests` | ✅ Resolved | Created `locustfile.py` simulating 6 users; validated SLAs (< 5s loading, < 2s updates) and created `performance_report.md`. |

## 4. Environment Setup & Installation

### Prerequisites

- Python 3.8+
- Virtual environment (`venv`)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/samarkand-fr/Python_Testing.git
   cd gudlft
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   export FLASK_APP=server.py
   flask run
   ```
   The application will be accessible at `http://127.0.0.1:5000/`.

---

## 3. Git Branching Strategy & Conventions

The project follows standard Git branching conventions:

### Branch Naming Format

`<type>/<descriptive-name>`

- `bug/<name>`: Bug fixes (e.g., `bug/login-email-crash`, `bug/points-redemption`)
- `feature/<name>`: New features (e.g., `feature/points-board`)
- `improvement/<name>`: Code quality and refactoring (e.g., `improvement/code-readability`)
- `test/<name>`: Test suite updates (e.g., `test/integration-booking-flow`)
- `perf/<name>`: Performance testing (e.g., `perf/locust-tests`)

### Key Branches

- **`master`**: Primary source of truth. Contains production-ready, fully tested code.
- **`qa`**: Dedicated code review / staging branch created from `master` for QA evaluation (not merged back into `master`).

---

## 4. Testing Suite

The project includes unit and integration tests grouped in separate folders under `tests/`.

### Running Tests

- **Run Unit Tests**:

  ```bash
  PYTHONPATH=. pytest tests/unit/
  ```

- **Run Integration Tests**:

  ```bash
  PYTHONPATH=. pytest tests/integration/
  ```

- **Run All Tests**:

  ```bash
  PYTHONPATH=. pytest tests/
  ```

### Code Coverage

The target coverage is **> 60%** (Currently achieved: **94%**).

To generate a coverage report:

```bash
PYTHONPATH=. pytest --cov=server --cov-report=term-missing tests/
```

---

## 5. Performance Testing (Locust)

Performance testing is configured using [Locust](https://locust.io/) simulating **6 concurrent users**.

### Performance SLAs

- **Competition List Fetching (`/showSummary`)**: Must load in **< 5 seconds**.
- **Points Update / Purchase (`/purchasePlaces`)**: Must execute in **< 2 seconds**.

### Running Performance Tests

1. Start the Flask application:

   ```bash
   export FLASK_APP=server.py
   flask run --port=5000
   ```

2. Run Locust in headless mode:

   ```bash
   locust -f locustfile.py --headless -u 6 -r 2 --run-time 10s --host http://127.0.0.1:5000
   ```

Detailed results are available in [`performance_report.md`](performance_report.md).

---

## 6. Project Architecture & Data Storage

The application uses lightweight JSON files as an in-memory data store:

- **`clubs.json`**: List of clubs, secretary emails, and point balances.
- **`competitions.json`**: List of competitions, dates, and available places.

---

## 7. External Documentation & Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Locust Performance Testing](https://docs.locust.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
