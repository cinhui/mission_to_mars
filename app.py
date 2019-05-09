from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db") 
# connect to mongo db and collection
#db = client.mars_db
#collection = db.mars_data

@app.route("/")
def home():
    #mars_data = list(db.collection.find())
    mars_data = mongo.db.collection.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scrape():
    #db.collection.remove({})
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)