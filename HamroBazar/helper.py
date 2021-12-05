from selenium import webdriver
from pathlib import Path
import re
import logging


def scrape_user(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        name = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr/td/center/h2')
        name = name.text.split(':')[1]
    except:

        logging.error('User Not Found')
        return None, 0, None

    try:
        post_count = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/table[2]/tbody/tr/td/font/b[3]').text
        first_post = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/table[5]/tbody/tr[1]/td[2]/center/a')
        first_post = first_post.get_attribute('href')

        driver.get(first_post)
        src = driver.page_source
        pattern = re.compile(r'98\d{8}')
        mobile_no = re.findall(pattern, src)[0]
    except:
        logging.error(f'{name} has no post')
        return name, 0, None

    driver.close()

    return name, post_count, mobile_no


def write_to_file(name, post_count, mobile_no, url):
    if not Path("data.csv").is_file():
        with open("data.csv", "w") as outfile:
            outfile.write("Name,Post Count,Mobile No\n")

    else:
        with open("data.csv", "a+") as outfile:
            outfile.write(name + "," + str(post_count) +
                          "," + mobile_no + "," + url + "," + "\n")
