from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS
from models.model1 import db, User_Info  #  Import db from model1 (don't redefine it!)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_master.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  #  Correctly initialize db with the app
api = Api(app)

# Route to Fetch Users
class UserResource(Resource):
    def get(self, user_id=None):
        """Fetch all users or a specific user by ID."""
        with app.app_context():
            if user_id:
                user = User_Info.query.get(user_id)
                if not user:
                    return {"message": "User not found"}, 404
                return jsonify({
                    "id": user.id, "email": user.email, "full_name": user.full_name,
                    "qualification": user.qualification, "dob": str(user.dob),
                    "flagged": user.flagged
                })

            users = User_Info.query.all()
            return jsonify([{
                "id": u.id, "email": u.email, "full_name": u.full_name,
                "qualification": u.qualification, "dob": str(u.dob),
                "flagged": u.flagged
            } for u in users])

    def post(self):
        """Add a new user."""
        data = request.get_json()
        if not data or not all(k in data for k in ["email", "password", "full_name", "qualification", "dob"]):
            return {"message": "Missing required fields"}, 400

        new_user = User_Info(
            email=data["email"],
            password=data["password"],  # Consider hashing passwords!
            full_name=data["full_name"],
            qualification=data["qualification"],
            dob=data["dob"],
        )
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
        return {"message": "User created successfully", "id": new_user.id}, 201

    def put(self, user_id):
        """Update an existing user's details."""
        with app.app_context():
            user = User_Info.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            data = request.get_json()
            if "email" in data:
                user.email = data["email"]
            if "password" in data:
                user.password = data["password"]  # Consider hashing passwords!
            if "full_name" in data:
                user.full_name = data["full_name"]
            if "qualification" in data:
                user.qualification = data["qualification"]
            if "dob" in data:
                user.dob = data["dob"]
            if "flagged" in data:
                user.flagged = data["flagged"]

            db.session.commit()
            return {"message": "User updated successfully"}, 200

    def delete(self, user_id):
        """Delete a user by ID."""
        with app.app_context():
            user = User_Info.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200

#  Register API routes
api.add_resource(UserResource, "/api/users", "/api/users/<int:user_id>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
