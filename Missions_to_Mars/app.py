from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
from jinja2 import Template
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_mission'
mongo = PyMongo(app)

@app.route('/')
def home():
    mars_info = mongo.db.mars_info.find_one()
    return render_template('index.html', mars_info = mars_info)

@app.route('/scrape')
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_image()
    mars_data = scrape_mars.scrape_weather()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hemi()
    mars_info.update({}, mars_data, upsert = True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)