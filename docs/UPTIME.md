# System Uptime and Health Verification

# BBMS-NF-002
Owner: Rithish P M (PR #1)

## Requirement Overview
Per SRS Section 4.2 and SAD Section 3.7, the Blood Bank Management System (BBMS) targets **99.5% operational availability** during standard service hours. This corresponds to an allowable unplanned downtime of no more than **3.6 hours per month**.

---

## Health Check Architecture

The system provides an automated health probe endpoint:
- **Endpoint**: `GET /api/health`
- **Authentication**: None (Publicly reachable for orchestrators, load balancers, and external synthetic monitors)
- **Response Format**: JSON
  ```json
  {
    "status": "healthy",
    "database": "connected",
    "service": "BBMS Backend API"
  }
  ```
- **Error Behavior**: If the underlying database connection fails, the probe returns HTTP 503 Service Unavailable:
  ```json
  {
    "status": "error",
    "database": "unhealthy",
    "detail": "Connection refused"
  }
  ```

---

## Uptime Strategy & Mitigation Mechanisms

1. **Synthetic Health Monitoring**:
   - Automated monitoring probes (e.g., UptimeRobot, Prometheus Blackbox Exporter, or AWS Route53 health checks) query `/api/health` at 60-second intervals.
   - Any non-200 status code triggers automated operational alerts.

2. **Process Management & Auto-Restart**:
   - In production containers or systemd environments, health check failures trigger automatic worker restarts.

3. **Database Resilience**:
   - Django database connection pooling and automatic reconnections maintain persistent database access.
   - Database operations are wrapped in atomic transactions with explicit row-level locking (`select_for_update`) to prevent locks and deadlocks.

4. **Independent Microservices**:
   - Non-critical external dependencies (such as the Node.js notification service) are architected as non-blocking async calls; outages in auxiliary services do not degrade the core BBMS request/donation workflow.

---

## Verification
Health check functionality is covered in the automated test suite:
```bash
python manage.py test bloodrequests.tests.test_health
```
