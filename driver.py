from selenium import webdriver
import time
from datetime import date
from selenium.webdriver.common.keys import Keys
from scrape_table import scrape_table
from return_dates import return_dates



#Open the link
browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.sharesansar.com/today-share-price")

#Select Commercial Bank
searchBar=browser.find_element_by_id('sector')
searchBar.send_keys('Commercial Bank')

sdate = date(2020, 1, 10)
edate = date(2020, 1, 20)
dates = return_dates(sdate,edate)
for day in dates:
    #Enter the date
    date_box = browser.find_elements_by_id('fromdate')
    date_box[0].clear()
    date_box[0].send_keys(day)
    #Click Search
    searchBar=browser.find_element_by_id('btn_todayshareprice_submit')
    searchBar.click()
    time.sleep(3) #Needed don't know why
    searchBar.send_keys(Keys.ENTER)
    time.sleep(5) #Wait for data to show up
    #Scrape the table
    html = browser.page_source
    if(scrape_table(data=html,date=day)):
        print(day,'Done')





