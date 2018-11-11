import pandas as pd 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests 
import os
import time
import pymongo

def scrape_Mars1():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    News_Title = soup.find('div', class_='content_title')
    News_Title= News_Title.text
    News_Title
    News_Paragraph = soup.find('div', class_='article_teaser_body')
    News_Paragraph = News_Paragraph.text
    News_Paragraph
    #----------------------------------
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('figure', class_='lede')
    full_size = img.find("a")["href"]
    browser.click_link_by_href(full_size)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find('img')['src']
    #--------------------------------------------
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    results = soup.find('div', class_="js-tweet-text-container")
    mars_weather = results.p.text
    #-----------------------------------------------
    url= "https://space-facts.com/mars/"
    mars_table = pd.read_html(url)
    mars_table
    df = mars_table[0]
    df.columns = ["Measurements", "Results"]
    df.set_index("Measurements", inplace=True)
    mars_html_table= df.to_html()
    df.to_html('table.html')
    #-------------------------------------------
    Url_List = []
    Hemispheres = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
    for Hemisphere in Hemispheres:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        browser.click_link_by_partial_text(Hemisphere)
        html = browser.html 
        soup = bs(html, 'html.parser')
        img_url = soup.find('div', class_="downloads").find('ul').find('li').find('a')['href']
        Url_List.append(img_url)
    Hem_List = [[Hemispheres[0], Url_List[0]],[Hemispheres[1], Url_List[1]],[Hemispheres[2], Url_List[2]],[Hemispheres[3], Url_List[3]]]
    lables = {0: "Title", 1: "Img_Url"}
    Hem_Dict = [{lables[idx]:val for idx,val in enumerate(item)} for item in Hem_List]
    H1 = Hem_Dict[0]
    H2 = Hem_Dict[1]
    H3 = Hem_Dict[2]
    H4 = Hem_Dict[3]
    scrape = {"News_Title": News_Title, "News_Paragraph": News_Paragraph, "Featured_Image": featured_image_url, "Mars_Tweet": mars_weather,
    "Mars_Table": mars_html_table,
     'Cerberus': H1["Title"], 'Cerberus_Img': H1["Img_Url"],
     'Schiaparelli': H2["Title"], 'Schiaparelli_Img': H2["Img_Url"],
     'Syrtis': H3["Title"], 'Syrtis_Img': H3["Img_Url"],
     'Valles': H4["Title"], 'Valles_Img': H4["Img_Url"],}
    return scrape

