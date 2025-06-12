from pymongo import MongoClient
import dotenv
import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
import datetime
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
users_collection = db.get_collection("users")
activiteiten_collection = db.get_collection("acictiviteiten")
inschrijven_collection = db.get_collection("inschrijvingen")
roles_collection = db.get_collection("roles")

app = Flask(__name__
            )  # Specify the folder for templates)

@app.route("/", methods=["GET"])
def home():
    # Serve the index.html template
    return render_template("index.html")

@app.route("/over_ons", methods=["GET"])
def over_ons():
    #server the overons.html template
    return render_template("overons.html")

@app.route("/login", methods = ["GET"])
def login():
    # Serve the login.html template
    return render_template("login.html")

@app.route("/contact", methods=["GET"])
def contact():
    #serve the contact.html tempplate
    return render_template("contact.html")

#register route
@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        technical_date = datetime.datetime.now()
        functional_date = technical_date.strftime("%A, %w %B, %Y")


        data = {"username" : username, "email" : email, "password" : password, "startdate" : functional_date}
        users_collection.insert_one(data)

        return redirect(url_for('login'))


    return render_template("register.html")

# Initiate server
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

