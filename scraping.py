from splinter import Browser

from bs4 import BeautifulSoup as soup

import pandas as pd 

import datetime as dt 


def scrape_all():
   
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
 
    news_title, news_paragraph= mars_news(browser)

    hemisphere_image_urls=hemisphere(browser)
    
    data={
        "news_title": news_title,

        "news_paragraph": news_paragraph,

        "featured_image": featured_image(browser),

        "facts": mars_facts(),

        "hemispheres": hemisphere_image_urls,

        "last_modified": dt.datetime.now()
    }

    
    browser.quit()

    return data


def mars_news(browser):

    
    url= 'https://mars.nasa.gov/news/'

    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html= browser.html 

    news_soup= soup(html, 'html.parser')

    try:

        slide_elem= news_soup.select_one('ul.item_list li.slide')

        news_title=slide_elem.find('div', class_= 'content_title').get_text()
      
        news_p= slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:

        return None,None

    return news_title, news_p


def featured_image(browser):

    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mar'

    browser.visit(url)

    full_image_elem= browser.find_by_id('full_image')[0]

    full_image_elem.click()

    browser.is_element_present_by_text('more info', wait_time=1)

    more_info_elem=browser.links.find_by_partial_text('more info')

    more_info_elem.click()

    html=browser.html

    img_soup=soup(html, 'html.parser')

    try:

        img_url_rel= img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:

        return None

    img_url= f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url


def mars_facts():
    
    try:
      
        df=pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:

        return None

    df.columns=['description', 'value']

    df.set_index('description', inplace=True)

    return df.to_html()


def hemisphere(browser):

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)


    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):

        hemisphere={}

        browser.find_by_css("a.product-item h3")[x].click()

        sample_img= browser.find_link_by_text("Sample").first

        hemisphere['img_url']=sample_img['href']

        hemisphere['title']=browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()

    return hemisphere_image_urls

if __name__== "__main__":
    
    print(scrape_all())





