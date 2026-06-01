# 🚀 QA + Security Automation Framework

> A full-stack **DevSecOps** solution integrating automated quality assurance and security testing into every stage of the CI/CD pipeline.

[![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/your-org/your-repo/pipeline.yml?label=CI%2FCD&logo=github-actions&logoColor=white)](https://github.com/your-org/your-repo/actions)
[![Security Scan](https://img.shields.io/badge/security-bandit%20%7C%20OWASP%20ZAP-brightgreen?logo=shield)](https://github.com/your-org/your-repo)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

This project demonstrates a **real-world DevSecOps workflow** used by modern engineering teams to enforce quality and security in every deployment. It combines automated API testing, browser-based UI testing, static code analysis, and dynamic vulnerability scanning — all orchestrated through GitHub Actions.

| Layer | Tool | Purpose |
|---|---|---|
| 🧪 API Testing | `pytest` + `requests` | Validate REST endpoints, status codes, response schemas |
| 🌐 UI Testing | `Selenium` + `pytest` | Cross-browser regression and smoke testing |
| 🔐 Static Analysis | `Bandit` | Identify Python security anti-patterns at commit time |
| 🕷️ Dynamic Scanning | `OWASP ZAP` | Runtime vulnerability detection (XSS, SQLi, OWASP Top 10) |
| ⚙️ CI/CD | `GitHub Actions` | Orchestrate all stages on push, PR, and schedule |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Developer Pushes Code                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  GitHub Actions Pipeline                 │
│                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐    │
│  │  Static  │   │   API    │   │   UI Automation  │    │
│  │ Analysis │──▶│  Tests   │──▶│   (Selenium)     │    │
│  │ (Bandit) │   │ (pytest) │   │                  │    │
│  └──────────┘   └──────────┘   └──────────────────┘    │
│                                         │               │
│                                         ▼               │
│                              ┌─────────────────┐        │
│                              │   OWASP ZAP     │        │
│                              │ Dynamic Scan    │        │
│                              └────────┬────────┘        │
│                                       │                 │
└───────────────────────────────────────┼─────────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │       Reports & Artifacts    │
                         │  • Test results (JUnit XML)  │
                         │  • Security report (JSON)    │
                         │  • ZAP HTML report           │
                         └─────────────────────────────┘
```

---

## 📁 Project Structure

```
qa-security-framework/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml          # Main GitHub Actions CI/CD pipeline
│
├── tests/
│   ├── api/
│   │   ├── conftest.py           # Fixtures, base URL, auth headers
│   │   ├── test_endpoints.py     # REST API test cases
│   │   └── test_schema.py        # Response schema validation
│   │
│   └── ui/
│       ├── conftest.py           # WebDriver setup / teardown
│       ├── pages/                # Page Object Model (POM) classes
│       │   ├── base_page.py
│       │   └── login_page.py
│       └── test_smoke.py         # UI smoke and regression tests
│
├── security/
│   ├── bandit.yaml               # Bandit static analysis config
│   └── zap/
│       ├── zap-baseline.conf     # ZAP baseline scan rules
│       └── zap-report.html       # Generated scan report (gitignored)
│
├── reports/                      # Generated test artifacts (gitignored)
│   ├── junit-api.xml
│   ├── junit-ui.xml
│   └── bandit-report.json
│
├── requirements.txt              # Python dependencies
├── pytest.ini                    # pytest configuration
└── README.md
```

---

## ⚙️ CI/CD Pipeline

The pipeline runs automatically on every `push` and `pull_request` to `main`. It has four sequential jobs, each gating the next.

```yaml
# .github/workflows/pipeline.yml

name: DevSecOps Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * *"   # Nightly full scan at 2 AM UTC

jobs:
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Bandit
        run: bandit -r . -c security/bandit.yaml -f json -o reports/bandit-report.json

  api-tests:
    needs: static-analysis
    runs-on: ubuntu-latest
    steps:
      - name: Run API Tests
        run: pytest tests/api/ --junitxml=reports/junit-api.xml -v

  ui-tests:
    needs: api-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run Selenium Tests (Headless Chrome)
        run: pytest tests/ui/ --junitxml=reports/junit-ui.xml -v

  dynamic-scan:
    needs: ui-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.11.0
        with:
          target: ${{ secrets.STAGING_URL }}
          rules_file_name: security/zap/zap-baseline.conf
          fail_action: true
```

---

## 🧪 API Testing

Tests are written with `pytest` and use the `requests` library to call live endpoints. All tests run against a configurable base URL via environment variable.

**Example test:**

```python
# tests/api/test_endpoints.py

import pytest, requests

BASE_URL = os.getenv("API_BASE_URL", "https://staging.example.com/api")

def test_get_users_returns_200():
    response = requests.get(f"{BASE_URL}/users", headers=auth_headers())
    assert response.status_code == 200

def test_create_user_schema():
    payload = {"name": "Test User", "email": "test@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload, headers=auth_headers())
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]
```

---

## 🌐 UI Testing (Selenium)

Browser tests follow the **Page Object Model** (POM) pattern for maintainability. Chrome runs in headless mode inside the Actions runner.

```python
# tests/ui/pages/login_page.py

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    SUBMIT_BTN    = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, username: str, password: str):
        self.find(self.USERNAME_FIELD).send_keys(username)
        self.find(self.PASSWORD_FIELD).send_keys(password)
        self.find(self.SUBMIT_BTN).click()
```

---

## 🔐 Static Security Analysis (Bandit)

Bandit scans all Python source files for common security issues on every commit. The pipeline **fails fast** if high-severity issues are detected.

```bash
# Run locally
bandit -r . -c security/bandit.yaml -f json -o reports/bandit-report.json

# View human-readable output
bandit -r . -ll   # Only medium and high severity
```

Bandit catches issues such as hardcoded credentials, use of `exec()`, insecure deserialization, weak cryptography, and SQL injection patterns.

---

## 🕷️ Dynamic Security Testing (OWASP ZAP)

The ZAP baseline scan runs against the deployed staging environment after all functional tests pass. It tests for the [OWASP Top 10](https://owasp.org/www-project-top-ten/) without active attack mode, making it safe for staging.

```bash
# Run ZAP scan locally with Docker
docker run -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://your-staging-url.com \
  -r zap-report.html \
  -J zap-report.json
```

Findings are exported as both an HTML report and a JSON file, uploaded as pipeline artifacts.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Chrome + ChromeDriver (matching version)
- Docker (for OWASP ZAP local runs)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/qa-security-framework.git
cd qa-security-framework

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the project root (never commit this file):

```env
API_BASE_URL=https://staging.example.com/api
APP_BASE_URL=https://staging.example.com
API_TOKEN=your_token_here
```

### Running Tests Locally

```bash
# All tests
pytest

# API tests only
pytest tests/api/ -v

# UI tests only
pytest tests/ui/ -v

# Static security scan
bandit -r . -c security/bandit.yaml
```

---

## 📊 Test Reports

All reports are generated as pipeline artifacts and retained for 30 days.

| Report | Format | Location |
|---|---|---|
| API test results | JUnit XML | `reports/junit-api.xml` |
| UI test results | JUnit XML | `reports/junit-ui.xml` |
| Bandit findings | JSON | `reports/bandit-report.json` |
| ZAP scan | HTML + JSON | `security/zap/zap-report.*` |

GitHub Actions automatically parses the JUnit XML files and displays pass/fail counts directly in the pull request summary.

---

## 🛡️ Security Policy

- All secrets are stored in **GitHub Actions Secrets** — never in code or config files
- The `security/bandit.yaml` config enforces a minimum severity threshold of `MEDIUM`
- ZAP scans are configured to fail the pipeline on `HIGH` or `CRITICAL` findings
- Dependency vulnerabilities are monitored via GitHub's Dependabot

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add new test for X'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request — the pipeline runs automatically

Please ensure all tests pass and Bandit reports no new high-severity findings before requesting a review.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Built to demonstrate real-world DevSecOps practices · Quality + Security · Every Deploy</sub>
</div>
