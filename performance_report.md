# Performance Test Report (Locust)

## Executive Summary
Performance testing was conducted using **Locust** to evaluate the Gudlift regional competition booking application under concurrent load, as specified in the Phase 2 requirements and Development Guide.

---

## Performance Threshold Requirements
1. **Competition List Retrieval / Loading (`POST /showSummary`)**:
   - **Requirement**: Must not exceed **5 seconds (5000 ms)**.
2. **Points Update / Booking (`POST /purchasePlaces`)**:
   - **Requirement**: Must not exceed **2 seconds (2000 ms)**.
3. **Simulated Load**:
   - **Default user count**: **6 concurrent users**.

---

## Test Configuration
- **Testing Tool**: Locust v2.46.1
- **Target Host**: `http://127.0.0.1:5001`
- **Simulated Users**: 6 concurrent users
- **Spawn Rate**: 2 users / second
- **Test Duration**: 10 seconds

---

## Test Results

### 1. Summary Metrics

| Endpoint | Method | Total Requests | Failures | Median Response Time | Average Response Time | Requirement Target | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Home Page** (`/`) | GET | 7 | 0 (0%) | 5 ms | 5.25 ms | N/A | **PASS** |
| **Public Points Board** (`/points`) | GET | 7 | 0 (0%) | 3 ms | 2.61 ms | N/A | **PASS** |
| **Competitions List** (`/showSummary`) | POST | 14 | 0 (0%) | 5 ms | 4.59 ms | **< 5,000 ms** | **PASS** |
| **Booking Form** (`/book/...`) | GET | 9 | 0 (0%) | 4 ms | 5.47 ms | N/A | **PASS** |
| **Update Points / Purchase** (`/purchasePlaces`) | POST | 5 | 0 (0%) | 5 ms | 5.06 ms | **< 2,000 ms** | **PASS** |
| **Total / Aggregated** | ALL | **42** | **0 (0%)** | **4 ms** | **4.61 ms** | N/A | **PASS** |

---

## Analysis & Conclusion

1. **Competitions List Retrieval**:
   - **Measured Average**: **4.59 ms**
   - **SLA Threshold**: **5,000 ms (5 s)**
   - **Result**: Passed easily (1000x faster than required threshold).

2. **Points Update Execution**:
   - **Measured Average**: **5.06 ms**
   - **SLA Threshold**: **2,000 ms (2 s)**
   - **Result**: Passed easily (400x faster than required threshold).

3. **Failure Rate**:
   - **0% failure rate** across all requests during concurrent execution.

The lightweight Flask architecture and in-memory JSON data structure deliver high throughput and response times well within the required limits.
