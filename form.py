from flask import Flask, render_template, request
from pymongo import MongoClient
import dotenv
import os

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

users_collection = db.get_collection("Users")

app = Flask(__name__)


@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        data = {"username" : username, "email" : email, "password" : password}
        users_collection.insert_one(data)

    
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
