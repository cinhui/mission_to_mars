from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

mars_dict = {}

def scrape():
    try: 

        browser = init_browser()

        # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        time.sleep(1)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # news_title = soup.find('div', class_='content_title').text
        # news_p = soup.find('div', class_='article_teaser_body').text

        results = soup.find_all('div', class_='list_text')
        news_title = results[0].find('div', class_="content_title").text
        news_p = results[0].find('div', class_="article_teaser_body").text
        
        print(news_title)
        print(news_p)
        mars_dict['news_title'] = news_title
        mars_dict['news_p'] = news_p

        # JPL Mars Space Images - Featured Image
        # Visit the url for JPL Featured Space Image 
        # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.
        # Use splinter to navigate the site and 
        # find the image url for the current Featured Mars Image and 
        # assign the url string to a variable called featured_image_url.
        # Make sure to find the image url to the full size .jpg image.
        # Make sure to save a complete url string for this image.
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)

        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(5)
        browser.click_link_by_partial_text('more info')
        time.sleep(5)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('img', class_='main_image').get('src')

        featured_image_url = "https://www.jpl.nasa.gov" + img_url
        print(featured_image_url)
        mars_dict['featured_image_url'] = featured_image_url 

        # Mars Weather
        # Visit the Mars Weather twitter account 
        # https://twitter.com/marswxreport?lang=en and 
        # scrape the latest Mars weather tweet from the page. 
        # Save the tweet text for the weather report as a variable called mars_weather.
        mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(mars_twitter_url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_weather = soup.find('p', class_='TweetTextSize').text
        tweet_link = soup.find('a', class_='twitter-timeline-link').text
        mars_weather = mars_weather.replace(tweet_link,'')
        print(mars_weather)
        mars_dict['mars_weather'] = mars_weather

        # Mars Facts
        # Visit the Mars Facts webpage https://space-facts.com/mars/ and 
        # use Pandas to scrape the table containing facts about the planet 
        # including Diameter, Mass, etc.
        facts_url = "https://space-facts.com/mars/"
        browser.visit(facts_url)

        tables = pd.read_html(facts_url)
        tables

        mars_facts_df = tables[0]
        mars_facts_df

        mars_facts_df.rename(columns = {0:'Description',1:'Value'}, inplace=True)
        mars_facts_df.set_index('Description', inplace=True)
        mars_facts_df

        # Use Pandas to convert the data to a HTML table string.
        mars_facts_html = mars_facts_df.to_html()
        # strip unwanted newlines to clean up the table
        # mars_facts_html.replace('\n', '')
        # print(mars_facts_html)

        mars_dict['mars_facts_html'] = mars_facts_html

        # Mars Hemispheres

        # Visit the USGS Astrogeology site 
        # https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars 
        # to obtain high resolution images for each of Mar's hemispheres.
        usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(usgs_url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # You will need to click each of the links to the hemispheres in order to find the 
        # image url to the full resolution image.
        # Save both the image url string for the full resolution hemisphere image, 
        # and the Hemisphere title containing the hemisphere name. 

        # Use a Python dictionary to store the data using the keys img_url and title.
        # Append the dictionary with the image url string and the hemisphere title to a list. 
        # This list will contain one dictionary for each hemisphere.
        hemispheres_image_urls = []
        mars_dict['hemispheres_image_urls'] = hemispheres_image_urls

        return mars_dict

    finally:
        browser.quit()
