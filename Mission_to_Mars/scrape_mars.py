#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time

def init_browser():
    # Executable path is where chromedriver.exe exists
    executable_path = {"executable_path": "c:\chromedriver\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_collection = {}
    
    browser = init_browser()
    
    ##  Mars News
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    time.sleep(2)

    # Use BeautifulSoup to write it into html
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    news = soup.find("div", class_="list_text")
    news_date = news.find("div", class_="list_date").text
    news_paragraph = news.find("div", class_="article_teaser_body").text
    news_title = news.find("div", class_="content_title").text

    print(f"Date: {news_date}")
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")

    # Store data in a dictionary
    mars_collection["news_date"] =news_date
    mars_collection["news_title"] = news_title
    mars_collection["news_paragraph"] = news_paragraph

    ## Mars Feature Image
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    print(featured_image_url)
    mars_collection["featured_image_url"] = featured_image_url

    ## Mars weather
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    time.sleep(2)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    mars_collection["mars_weather"] = mars_weather
 
    ## Mars Facts
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)[1]
    mars_data = pd.DataFrame(table)
    mars_data.columns = ["Mars Facts", "Values"]
    print(mars_data)
    mars_html_table = mars_data.to_html(index=False)
    mars_collection["fact_table"] = mars_html_table
 
   ## Mars Hemispheres
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemispheres = []
  
    ## loop through the four tags and load the data to the dictionary
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemispheres.append(dictionary)
        browser.back()   

        mars_collection["hemisphere_image"] = mars_hemispheres

    browser.quit()
    return mars_collection