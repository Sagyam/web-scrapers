browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://basobaas.com/properties/for-sale/all/house")

def scroll_till_end(browser):
    def scroll(browser):
        browser.execute_script("window.scrollTo(0, window.scrollY + 200)")

    def load_more(browser):
        load_more = browser.find_element_by_xpath('//*[@id="loadingBtn"]')
        load_more.click()

    def read_button_text(browser):
        btn = browser.find_element_by_xpath('//*[@id="loadingBtn"]')
        return btn.text

    while read_button_text(browser) == 'LOAD MORE PROPERTY':
        scroll(browser)
        load_more(browser)
        time.sleep(5)

listings = browser.find_element_by_xpath('//*[@id="listing"]/div/div/div[3]/div/div[2]')
cards = listings.find_elements_by_tag_name('a')
print(len(cards), " Links Found")
links = []
for card in cards:
    link = card.get_attribute('href')
    if type(link) == type('string'):    #Avoid ads
        link = str(link)
        if link.find('premium') == -1: #Premium properties have different layout
            links.append(link)
