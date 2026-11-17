"""
Tourist API with token validation

Provides a PUT endpoint to update a tourist record.
Token validation expects a header named ``Check-Token`` containing a pre‑generated
valid token. If the token is missing or invalid a *500 Internal Server Error*
is returned (as required by the task description).

The API is built with Flask‑RESTX which also exposes a Swagger UI at ``/``.
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# In a real deployment the token would be stored securely.
# Replace ``YOUR_VALID_TOKEN`` with the actual token value.
VALID_TOKEN = os.getenv("TOURIST_API_TOKEN", "test-token-123")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "tourists.db")

app = Flask(__name__)
# SQLite for simplicity – the file will be created automatically.
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app, version="1.0", title="Tourist API", description="Update tourist records with token validation")
ns = api.namespace("tourists", path="/api/tourists")

db = SQLAlchemy(app)

# ---------------------------------------------------------------------------
# Database model
# ---------------------------------------------------------------------------
class Tourist(db.Model):
    __tablename__ = "tourists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=True)
    contact_details = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "destination": self.destination,
            "contact_details": self.contact_details,
        }

# ---------------------------------------------------------------------------
# API payload model (Swagger documentation)
# ---------------------------------------------------------------------------
tourist_update_model = api.model("TouristUpdate", {
    "name": fields.String(description="Tourist's name"),
    "destination": fields.String(description="Visited destination"),
    "contact_details": fields.String(description="Contact information"),
})

# ---------------------------------------------------------------------------
# Helper – token validation
# ---------------------------------------------------------------------------
def validate_token():
    token = request.headers.get("Check-Token")
    if token != VALID_TOKEN:
        # The specification asks for a 500 on invalid token.
        api.abort(500, "Invalid or missing token")

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@ns.route("/<int:id>")
class TouristResource(Resource):
    @api.doc(description="Update an existing tourist record")
    @api.expect(tourist_update_model, validate=True)
    def put(self, id):
        """Update tourist fields after token validation.

        1. Validate the ``Check-Token`` header.
        2. Fetch the existing record – 404 if not found.
        3. Apply any supplied fields.
        4. Commit and return a success message.
        """
        # Step 1 – token validation
        validate_token()

        # Step 2 – fetch record
        tourist = Tourist.query.get(id)
        if not tourist:
            api.abort(404, f"Tourist with id {id} not found")

        # Step 3 – update mutable fields
        payload = request.json or {}
        if "name" in payload:
            tourist.name = payload["name"]
        if "destination" in payload:
            tourist.destination = payload["destination"]
        if "contact_details" in payload:
            tourist.contact_details = payload["contact_details"]

        # Step 4 – persist changes
        db.session.commit()
        return {"message": "Tourist Updated Successfully"}, 200

# ---------------------------------------------------------------------------
# Initialise database (create tables if they don't exist)
# ---------------------------------------------------------------------------
@app.before_first_request
def create_tables():
    db.create_all()
    # Insert a dummy tourist for demonstration if the table is empty.
    if Tourist.query.first() is None:
        demo = Tourist(name="John Doe", destination="Paris", contact_details="john@example.com")
        db.session.add(demo)
        db.session.commit()

if __name__ == "__main__":
    # Run on localhost:5000 – Swagger UI is accessible at http://127.0.0.1:5000/
    app.run(debug=True)
