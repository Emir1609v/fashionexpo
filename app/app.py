from pymongo import MongoClient
import dotenv
import os
from flask import Flask, jsonify, request, render_template

# Load environment variables from .env file
dotenv.load_dotenv()

# Get the MongoDB connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not set.")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Check if the connection is successful
try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)  # Exit the program if the connection fails

# Access the database
db = client.get_database("fashionexpo")

# Access the collections
users_collection = db.get_collection("Users")
activiteiten_collection = db.get_collection("Activiteiten")
inschrijven_collection = db.get_collection("inschrijvingen")
roles_collection = db.get_collection("roles")

app = Flask(__name__
            )  # Specify the folder for templates)

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

# Initiate server
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

