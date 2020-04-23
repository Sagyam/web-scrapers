from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from scraper import scrape
scrape('https://basobaas.com/property/house-for-sale-in-mandikatar-6147')
'''
#Open the link
browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://basobaas.com/properties/for-sale/all/apartment")

#helper func
def scroll_and_wait(browser):
    browser.execute_script("window.scrollTo(0, window.scrollY + 200)")
    time.sleep(1)

def load_more(browser):
    load_more = browser.find_element_by_xpath('//*[@id="loadingBtn"]')
    load_more.click()
    time.sleep(3)

def read_button(browser):
    btn = browser.find_element_by_xpath('//*[@id="loadingBtn"]')
    print(btn.text)
    return btn.text

#Load all properties
while read_button(browser) == 'LOAD MORE PROPERTY':
    scroll_and_wait(browser)
    load_more(browser)

listings = browser.find_element_by_xpath('//*[@id="listing"]/div/div/div[3]/div/div[2]')
cards = listings.find_elements_by_tag_name('a')
print(len(cards)," Links Found")
for card in cards:
    link = card.get_attribute('href')
    if type(link) == type('string'):
        scrape(link)
    break    
'''
#browser.close()