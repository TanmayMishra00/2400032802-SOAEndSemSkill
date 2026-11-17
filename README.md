# Tourist API

This repository contains a Flask‑RESTX application that provides a **PUT** endpoint to update a tourist record.

## Features
- SQLite database (`tourists.db`) with a simple `Tourist` model.
- Token validation via the `Check-Token` header. The token value is read from the environment variable `TOURIST_API_TOKEN`. If the header is missing or does not match, the API returns **500 Internal Server Error** as required by the task.
- Swagger UI (via Flask‑RESTX) available at `http://127.0.0.1:5000/` for interactive testing.
- A dummy tourist record is created on first run so you can immediately test the update endpoint.

## Prerequisites
- Python 3.8+ (the code was tested with Python 3.11).
- `pip` to install dependencies.

## Setup
```bash
# Clone or copy the files into a directory, e.g. C:\Users\tanma\tourist_api
cd C:\Users\tanma\tourist_api

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate  # on Windows

# Install required packages
pip install -r requirements.txt
```

## Configuration
Set the environment variable `TOURIST_API_TOKEN` to the token value you want to accept:
```bash
# PowerShell example
$env:TOURIST_API_TOKEN = "<your-token-here>"
```
If the variable is not set, the code falls back to the placeholder `YOUR_VALID_TOKEN`. **Replace that placeholder** in `app.py` with your actual token or set the environment variable as shown above.

## Run the API
```bash
python app.py
```
The server starts on `http://127.0.0.1:5000/`. Open that URL in a browser to see the Swagger UI.

## Example: Update a tourist record
Assuming the dummy record has `id = 1`:
```bash
curl -X PUT "http://127.0.0.1:5000/api/tourists/1" \
  -H "Content-Type: application/json" \
  -H "Check-Token: <your-token-here>" \
  -d '{"destination": "Tokyo", "contact_details": "john.doe@example.com"}'
```
A successful request returns:
```json
{"message": "Tourist Updated Successfully"}
```
If the token is missing or incorrect, the response is:
```json
{"message":"Invalid or missing token"}
```
with HTTP status **500**.

## Testing with the built‑in Flask test client
You can run the following script to programmatically verify the behavior:
```python
import os, json
from app import app, VALID_TOKEN

client = app.test_client()

# Valid token test
resp = client.put(
    '/api/tourists/1',
    json={"destination": "Rome"},
    headers={"Check-Token": VALID_TOKEN},
)
print('Valid token response:', resp.status_code, resp.json)

# Invalid token test
resp = client.put(
    '/api/tourists/1',
    json={"destination": "Berlin"},
    headers={"Check-Token": "bad-token"},
)
print('Invalid token response:', resp.status_code, resp.json)
```
Run it with `python test_update.py` (create the file and add it to the repo).

## Directory layout
```
 tourst_api/
 ├─ app.py            # Flask application (the main code you will run)
 ├─ requirements.txt  # Python dependencies
 └─ README.md         # This file
```

---
**Note:** The current sandbox environment does not have a functional Python interpreter, so the `pip install` and `python app.py` commands cannot be executed here. Please run the steps on your local machine.
