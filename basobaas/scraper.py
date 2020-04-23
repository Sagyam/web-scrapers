from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import regex
import csv  

#Open the link
def scrape(link):
    browser = webdriver.Chrome()
    browser.minimize_window()
    browser.get(link)
    title,address,city = title_and_address(browser)
    price,bedroom,bathroom,floors,parking = basic_details(browser)
    face,year,views,area,road,road_width,road_type,build_area,posted = overview(browser)
    amenities = get_amenities(browser)
    printer(title,address,city,price,bedroom,bathroom,floors,parking,face,year,views,area,road,road_width,road_type,build_area,posted,amenities)
    browser.close()

#Categories
def title_and_address(browser):
    title = browser.find_elements_by_class_name('title-price')
    title = title[0].find_element_by_tag_name('h1')
    address = browser.find_elements_by_class_name('address')
    address = address[0].text
    city = city_name(address)
    return(title.text,address,city)

def basic_details(browser):
    price = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[1]/div/div/div[1]/div[2]')
    price = regex.get_price(price.text)
    bedroom = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]')
    bathroom = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div[2]/div[2]')
    floors = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/div[2]')
    parking = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div[4]/div[2]')
    return(price,bedroom.text,bathroom.text,floors.text,parking.text)

def overview(browser):
    upper = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]')
    lower = browser.find_element_by_xpath('//*[@id="details-prop"]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]')
    face,year,views = regex.get_upper(upper.text)
    area,road,road_width,road_type,build_area,posted = regex.get_lower(lower.text)
    return face,year,views,area,road,road_width,road_type,build_area,posted

def get_amenities(browser):   
    try:
        amenities_list = []
        amenities_section = browser.find_elements_by_class_name('amenities')
        amenities = amenities_section[0].find_elements_by_tag_name('li')
    except IndexError:
        return amenities_list
    for am in amenities:
        amenities_list.append(am.text)
    return amenities_list


def city_name(address):
    word_list = address.split()
    return word_list[-1]


def printer(title,address,city,price,bedroom,bathroom,floors,parking,face,year,views,area,road,road_width,road_type,build_area,posted,amenities):
    print('Title:',title)
    print('Address:',address)
    print('City:',city)
    print('Price:',price)
    print('Floors:',floors)
    print('Parking Space:',parking)
    print('Bedroom:',bedroom)
    print('Bathroom:',bathroom)
    print('********************************************************************************')
    print('Face:',face)
    print('Year:',year)
    print('Views:',views)
    print('Area:',area)
    print('Road Width:',road_width)
    print('Road Type:',road_type)
    print('Build Area:',build_area)
    print('Posted:',posted)
    print('********************************************************************************')
    for amenity in amenities:print(amenity)

def reader(title,address,city,price,bedroom,bathroom,floors,parking,face,year,views,area,road,road_width,road_type,build_area,posted,amenities):
    filename = 'basobbas.csv'
    try:
        file = open(filename, 'r')
        file.close()
    except IOError:
        file = open(filename, 'w')
        file.close()
    with open(filename,'a') as file:
         pass
    
