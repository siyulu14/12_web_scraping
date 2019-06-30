from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_mars"
mongo = PyMongo(app)


#  create route that renders index.html template
@app.route("/")
def index():

    mars = mongo.db.collection.find_one()
    
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():

    mars = mongo.db.collection
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

