from pymongo import mongo_client
from flask import Flask, jsonify, request, render_template

main = blueprint("main", __name__)

@app.route("/")
def home():
    # Serve the index.html template
    return render_template("index.html")

@app.route("/users", methods=["GET"])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))  # Exclude MongoDB _id from output
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    required_fields = ['username', 'email', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing one of the required fields: {required_fields}"}), 400
    
    users_collection.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201