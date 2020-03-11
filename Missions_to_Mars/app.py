from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import pymongo
from jinja2 import Template
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_info
collection = db.mars_data

@app.route('/')
def home():
    mars_info = client.db.mars_info.find_one()
    return render_template('index.html', mars_info = mars_info)

@app.route('/scrape')
def scrape():
    mars_info = client.db.mars_info
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_image()
    mars_data = scrape_mars.scrape_weather()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hemi()
    db.collection.updateOne({},mars_data,{upsert: True})
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)