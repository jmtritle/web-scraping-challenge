# downloading dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless = True)

mars_info = {}

def scrape_news():

    # setting the news_url and rigging up both requests and beautifulsoup
    news_url = 'https://mars.nasa.gov/news/'
    news_response = requests.get(news_url)
    soup = bs(news_response.text, 'lxml')
    # getting the title from the appropriate div and class
    news_title = soup.find('div', class_ = 'content_title').text
    # getting the first paragraph information from the appropriate div and class
    news_p = soup.find('div', class_ = 'rollover_description_inner').text
    mars_info['mars_headline'] = news_title
    mars_info['mars_text'] = news_p

    return mars_info

def scrape_image():
    browser = init_browser()
    # loading the image site's url
    image_site_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # visiting the site via splinter
    browser.visit(image_site_url)

    # clicking through the site via splinter to get to the large image
    browser.click_link_by_id('full_image')
    browser.click_link_by_partial_href('details')

    # finally getting to the large image via splinter
    browser.click_link_by_partial_href('largesize')

    # saving the url to f_image_url
    featured_image_url = browser.url
    mars_info['featured_img_url'] = featured_image_url

    return mars_info

def scrape_weather():
    # loading the twitter page for martian weather and rigging up some beautiful soup
    mars_weather_url ='https://twitter.com/marswxreport?lang=en'
    weather_response = requests.get(mars_weather_url)
    w_soup = bs(weather_response.text, 'lxml')

    # looking for the correct div and class, then pulling the text from the first paragraph within that container/class
    mars_tweets = w_soup.find('div', class_ = 'stream').find_all(class_ = 'js-stream-item')
    for tweet in mars_tweets:
        mars_text = tweet.find('div', class_ = 'js-tweet-text-container').p.text
        if 'InSight sol' in mars_text:
            mars_weather = mars_text.strip()
    mars_info['mars_weather'] = mars_weather

    return mars_info

def scrape_facts():
    # loading the mars facts url and getting pandas to read the page
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_raw = pd.read_html(mars_facts_url)

    # moving the raw facts into a new variable
    mars_df = mars_facts_raw[0]

    # adding column names and setting the index
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace = True)

    # transforming the table to html and saving that to a variable
    mars_table_data = mars_df.to_html()
    mars_info['mars_facts'] = mars_table_data

    return mars_info

def scrape_hemi():
    browser = init_browser()
    # setting up the mars hemisphere urls and visiting the site
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_hemi_url = 'https://astrogeology.usgs.gov/'
    browser.visit(mars_hemi_url)

    # making some more beautifulsoup to get the hemisphere information
    hemi_response = requests.get(mars_hemi_url)
    h_soup = bs(hemi_response.text, 'lxml')

    # setting up the hemisphere_image_urls dictionary
    hemisphere_image_urls = []

    # getting a list of the image links (products)
    products = soup.find('div', class_ = 'result-list')
    hemispheres = products.find_all('div', class_ = 'item')

    # setting up the for loop to pull the information on all four image links
    for hemisphere in hemispheres:
    
        # getting the title for each item
        title = hemisphere.find('h3').text
    
        # getting the partial link attached to each item and creating a full link
        partial_link = hemisphere.find('a')['href']
        image_link = base_hemi_url + partial_link
    
        # using splinter to go to the link and get the html to add to the beautifulsoup that's a-stewin'
        browser.visit(image_link)
        hemi_html = browser.html
        h_soup_2 = bs(hemi_html, 'lxml')
    
        # using this new iteration of soup to find the link affiliated with downloads
        downloads = h_soup_2.find('div', class_ = 'downloads')
        image_url = downloads.find('a')['href']
    
        # loading the whole, hot mess into the dictionary generated earlier
        hemisphere_image_urls.append({'title': title, 'img_url': image_url})

        mars_info['hemi_img_url'] = hemisphere_image_urls
        return mars_info
    print(mars_info)