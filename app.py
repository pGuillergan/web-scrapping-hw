from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
	feat_img = scrape_mars.scrape_featured()
	weather = scrape_mars.scrape_weather()
	hemi = scrape_mars.scrape_hemispheres()
	#fetch news data from mongodb
	news_data = mongo.db.collection_news.find()
	profile, comp = scrape_mars.scrape_facts()

	return render_template("index.html", 
		feat_img=feat_img, 
		weather=weather, 
		hemi=hemi, 
		news_data=news_data, 
		profile=profile, 
		comp=comp)



if __name__ == "__main__":
    app.run(debug=True)
