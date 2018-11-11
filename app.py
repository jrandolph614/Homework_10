from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data = mongo.db.collection.find()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    scrape = scrape_mars.scrape_Mars1()
    mars_info = mongo.db.collection
    mars_info.update({}, scrape, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)