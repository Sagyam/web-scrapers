import requests
from bs4 import BeautifulSoup

# get the data
data = requests.get('https://www.sharesansar.com/today-share-price')

# load data into bs4
soup =BeautifulSoup(data.text, 'html.parser')

# extract only the table from page
table = soup.find('table', { 'id': 'headFixed' })
tbody = table.find('tbody')

# Intilalize variables
head_row =[
    'Serial_no',
    'Symbol',
    'Confidence',
    'Open',
    'High',
    'Close'
]
# Create a new file and write title row
with open('today_price.csv', "w") as outfile:
        outfile.write(str(head_row))
        outfile.write("\n")

row_data = []

for tr in tbody.find_all('tr'):
    Serial_no = tr.find_all('td')[0].text.strip()
    symbol = tr.find_all('td')[1].text.strip()
    stock_confidence = tr.find_all('td')[2].text.strip()
    open_price = tr.find_all('td')[3].text.strip()
    high_price = tr.find_all('td')[4].text.strip()
    low_price  = tr.find_all('td')[5].text.strip()
    close_price= tr.find_all('td')[6].text.strip()
    row_data.append(Serial_no)
    row_data.append(symbol)
    row_data.append(stock_confidence)
    row_data.append(open_price)
    row_data.append(high_price)
    row_data.append(low_price)
    row_data.append(close_price)
    print(row_data)

    with open('today_price.csv', "a+") as outfile:
        outfile.write(str(row_data))
        outfile.write("\n")

    row_data.clear()