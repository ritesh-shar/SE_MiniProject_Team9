# BBMS Test and Evaluation Reports

This directory contains automated verification reports for the Blood Bank Management System (Team 9), generated per academic evaluation criteria:

- `unit_test_report.md`: Detailed breakdown of all acceptance test cases (TC-*) and Django test runner execution.
- `system_validation_report.md`: End-to-end flow driver execution validating all 19 functional and non-functional requirements.
- `code_coverage_report.txt`: Statement code coverage analysis.
- `branch_coverage_report.txt`: Branch decision code coverage analysis.
- `htmlcov/`: Interactive HTML code coverage inspection site (open `index.html` in browser).

---

## Regeneration Instructions

To regenerate all reports from a fresh environment:

```bash
# 1. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 2. Run database migrations
python manage.py migrate

# 3. Execute report generation orchestrator
python scripts/generate_reports.py
```
