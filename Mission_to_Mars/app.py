# Import modules
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Set up Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Home Page
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and mars data
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():

    # Call the scrape  in scrape_mars.py
    mars_scrape = scrape_mars.scrape()

    # Update the Mongo database
    mongo.db.collection.update({}, mars_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)