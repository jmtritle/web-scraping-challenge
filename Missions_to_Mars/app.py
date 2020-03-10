from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_info_items

@app.route('/')
def home():
    mars_info = list(db.collection.find())[0]
    return render_template('index.html', mars_info = mars_info)

@app.route('/scrape')
def scrape():
    db.collection.remove({})
    mars_info = scrape_mars.scrape()
    db.collection.insert_one(mars_info)
    return render_template('scrape.html')

if __name__ == "__main__":
    app.run(debug=True)