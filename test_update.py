import os
from app import app, VALID_TOKEN

# Ensure the app context is pushed for DB operations
with app.app_context():
    client = app.test_client()

    # Valid token test
    resp = client.put(
        '/api/tourists/1',
        json={"destination": "Rome", "contact_details": "john.rome@example.com"},
        headers={"Check-Token": VALID_TOKEN},
    )
    print('Valid token status:', resp.status_code)
    print('Response JSON:', resp.get_json())

    # Invalid token test
    resp = client.put(
        '/api/tourists/1',
        json={"destination": "Berlin"},
        headers={"Check-Token": "invalid-token"},
    )
    print('Invalid token status:', resp.status_code)
    print('Response JSON:', resp.get_json())
