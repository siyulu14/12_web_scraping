# dependency
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd 
import time

def init_browser():
    executable_path = {"executable_path": "/Users/David W. Jones/class/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # use splinter to visit url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # save page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # save the most recent news, title and date
    news = soup.find("div", class_="list_text")
    news_date = news.find("div", class_="list_date").text
    news_title = news.find("div", class_="content_title").text
    news_p = news.find("div", class_="article_teaser_body").text

    # Add the news date, title and summary to the mars data
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    # visit the JPL Mars URL
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # save page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the image and image url
    image = soup.find("img", alt="Landing in Oxia Palus")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image

    # Add the featured image url to the mars data
    mars_data["featured_image_url"] = featured_image_url

    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    # save page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the weather information
    tweets = soup.find('div', class_="js-tweet-text-container")
    mars_weather = tweets.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Add the weather to the mars data
    mars_data["mars_weather"] = mars_weather

    # Visit the Mars facts webpage and scrape table data into Pandas
    url3 = "http://space-facts.com/mars/"

    tables = pd.read_html(url3)
    mars_dt = tables[0]
    mars_dt.colums = ['parameter', 'data']
    mars_dt = mars_dt.rename(columns = {0:'parameter', 1:'data'})
    mars_dt = mars_dt.set_index("parameter")
    marsdt = mars_dt.to_html(classes='marsdata')
    marsdt = marsdt.replace('\n', ' ')
    
    # Add the Mars facts table to the mars data
    mars_data["mars_table"] = marsdt

    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)

    # Use splinter to load and loop through the 4 images and load them into a dictionary
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]

    import time
    for i in range (4):

        time.sleep(1)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    
    mars_data['mars_hemis'] = mars_hemis
    # Return the dictionary
    return mars_data

