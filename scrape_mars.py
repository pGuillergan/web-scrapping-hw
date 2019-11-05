from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import pymongo

def init_browser():
	#----------for mac
	#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	#browser = Browser('chrome', **executable_path, headless=False)
	#----------for windows
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', **executable_path, headless=False)
#--------------------------------------------------------------------------------
# returns a list of dictionaries with 3 entries
def scrape_news():
	url = "https://mars.nasa.gov/news/"
	browser =  init_browser()
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	results = soup.find_all('li', class_='slide')
	news_list = []
	for res in results:
		title = res.find('div', class_='content_title').text
		date = res.find('div', class_='list_date').text
		teaser = res.find('div', class_='article_teaser_body').text
		news_list.append({"date":date, "title":title, "teaser":teaser})   
	browser.quit()
	return news_list
#--------------------------------------------------------------------------------
# returns a string of a link to an image online
def scrape_featured():
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser =  init_browser()
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	data_link = soup.find('a', id='full_image')['data-link']
	base_url = "https://www.jpl.nasa.gov"
	browser.visit(base_url+data_link)
	html = browser.html
	soup = bs(html, 'html.parser')
	hi_res = soup.find('figure', class_='lede').a['href']
	browser.quit()
	return base_url + hi_res
#--------------------------------------------------------------------------------
# returns a paragraph string
def scrape_weather():
	url = "https://twitter.com/marswxreport?lang=en"
	browser =  init_browser()
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	timeline = soup.find('div', class_='ProfileTimeline')
	tweet_panel = timeline.find('div', class_='content')
	date = tweet_panel.find('small', class_='time').a.text
	tweet = tweet_panel.find('div', class_='js-tweet-text-container').p.text
	latest_tweet = f'Latest Tweet from Mars Weather:\n  {date} - {tweet}'
	browser.quit()
	return latest_tweet
#--------------------------------------------------------------------------------
def scrape_facts():
	import pandas as pd
	url = "https://space-facts.com/mars/"
	html = pd.read_html(url)
	return html
#--------------------------------------------------------------------------------
#return list of dicts with 2 entries
def scrape_hemispheres():
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser =  init_browser()
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	hemisphere_image_urls = []
	base_url = 'https://astrogeology.usgs.gov'
	prods = soup.find('div', class_='collapsible results').find_all('div', class_='description')
	for i in prods:
		link = base_url + i.a['href']
		browser.visit(link)
		html_sub = browser.html
		soup_sub = bs(html_sub, 'html.parser')
		title = soup_sub.find('div', class_='content').find('h2', class_='title').text
		title = title.strip("Enhanced")
		link_ext = soup_sub.find('div', class_='wide-image-wrapper').find('img', class_='wide-image')['src']
		img_url = base_url + link_ext
		hemisphere_image_urls.append({"title":title, "img_url":img_url})
	browser.quit()
	return hemisphere_image_urls
