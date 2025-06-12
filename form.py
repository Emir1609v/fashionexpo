from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import dotenv
import os
import datetime


dotenv.load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not set.")


client = MongoClient(MONGO_URI)


try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)  


db = client.get_database("fashionexpo")

users_collection = db.get_collection("Users")

app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(debug=True)
