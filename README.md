## Brute Force Detection Simulator — Backend

## Live At

<p align="center">
    <a href="https://bfds-backend.onrender.com/">
        <img src="https://img.shields.io/badge/Try_it_Out-10B981?style=for-the-badge&logo=rocket&logoColor=white" alt="Try it Out">
    </a>
</p>

- <q><b>The backend deployed on free tier render so you could see a cold start</b> </q>

<br>
<br>


A small FastAPI backend that demonstrates a brute-force login detector, cookie-based JWT authentication, and an alerting daemon scaffold. It can be used as a learning/demo service for detecting repeated failed login attempts and blocking offending IPs.

Also:
    - https://github.com/TheGoodUser/brute-force

Key points:

- FastAPI app serving login/logout/protected endpoints
- Simple in-memory brute-force detector that blocks IPs after repeated rapid failed attempts
- Alert daemon scaffolded for SendGrid-based notifications (`alert/alert_daemon.py`)

---

## Why this is useful

- Shows a compact example of integrating authentication (JWT in cookies) with a monitoring/mitigation component.
- Useful for learning about: FastAPI, JWT cookies, simple rate/attack detection, and how to scaffold alerting.
- Small and easy to run locally for testing or demonstration.

## Features

- POST /login — accepts form fields and issues an HTTP-only access_token cookie on success
- POST /logout — deletes the cookie
- GET /protected — example protected route powered by a cookie JWT dependency
- BruteForceDetector — a tiny detector that tracks rapid repeated requests and blocks the source IP
- Alert daemon (placeholder) — template to send emails via SendGrid

## Quick start (Windows PowerShell)

Assumptions and notes:

- This repository contains a pre-existing virtual environment folder `backend-venv/`. For reproducibility we recommend creating and using a fresh virtual environment.
- The app expects a few environment variables for production features (see "Environment variables" below). A development run can work with defaults in the code (for example, a demo user is defined in `main.py`).

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Note: `fastapi[standard]` in `requirements.txt` includes `uvicorn` so you can run the app with uvicorn.

3. Run the development server:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000/docs for the OpenAPI UI.

## Environment variables

The repository uses dotenv in several places. Create a `.env` in the project root (or set OS env vars) to configure these values:

- SENDGRID_API_KEY — API key for SendGrid if you enable the alerting code in `alert/alert_daemon.py`
- SENDER_EMAIL — sender address used by the alert daemon
- IS_PRODUCTION — set to `true` or `1` in production to make cookies secure

Security note: `main.py` currently contains a demo `SECRET_KEY` value and a hard-coded demo user. For production, set and store a secure `SECRET_KEY` in environment variables and replace demo credentials.

## Demo credentials (development only)

The app includes a demo user in `main.py`. Use these values for local testing only:

- email: `ram19870101@gmail.com`
- password: `Test@123`

Example login (PowerShell using curl):

```powershell
curl -X POST -F "email=ram19870101@gmail.com" -F "password=Test@123" http://127.0.0.1:8000/login -i
```

If login succeeds the server sets an HTTP-only cookie called `access_token`. You can then call the protected route:

```powershell
curl --cookie "access_token=<cookie-value>" http://127.0.0.1:8000/protected
```

Or use the interactive docs at `/docs` which let you exercise the endpoints.

## Where to look in the code

- `main.py` — FastAPI app and routes
- `functions/jwt_generation.py` — helper to create JWT access tokens
- `functions/get_current_user.py` — dependency that reads the cookie and decodes JWT
- `monitoring/attacks/brute_force/brute_force_detector.py` — simple in-memory detector and blocker
- `alert/alert_daemon.py` — SendGrid alert template (commented-out send logic)

## How it detects attacks

The `BruteForceDetector` measures the time between consecutive requests and increments an attack counter when requests arrive faster than a configured latency threshold. When the counter reaches a threshold the detector appends the offending IP to the in-memory `blocked_ips` list and calls the alert stub.

This is intentionally small and in-memory so you can reason about the flow; in production you would replace it with a persistent/centralized store and more robust rate-limiting logic.

## Contributing and support

- For simple issues or questions, open an issue in this repository.
- If you want to contribute code, please open a pull request and include tests where appropriate.
- For contribution guidelines or a code of conduct, add `CONTRIBUTING.md` or `CODE_OF_CONDUCT.md` to the repo and link them from here.

## Maintainers

This project is maintained in the `TheGoodUser/bfds-backend` repository. If you need help, open an issue or reach out to the repository maintainers.

## License

This file does not contain license text. See the repository `LICENSE` file if present.

---

If you'd like, I can also:

- add a minimal `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` template,
- wire up a tiny unit test that validates the demo login flow,
- or convert the hard-coded `SECRET_KEY` into a configured `.env` lookup (low-risk change).
