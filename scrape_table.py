import requests
from bs4 import BeautifulSoup

def scrape_table(data,date):

    # load data into bs4
    soup =BeautifulSoup(data, 'html.parser')

    # extract only the table from page
    table = soup.find('table', { 'id': 'headFixed' })
    tbody = table.find('tbody')

    #Check for empty table
    row_count = len(tbody.find_all('tr'))
    if row_count < 2:
        print("No record for ",date)
        return False
    

    # Intilalize variables
    head_row =[
        'Serial_no',
        'Symbol',
        'Confidence',
        'Open',
        'High',
        'Close',
        'Date'
    ]
    # Create a new file and write title row
 
    filename = date + '.csv'
    with open(filename, "w") as outfile:
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
        row_data.append(date)

        with open(filename, "a+") as outfile:
            outfile.write(str(row_data))
            outfile.write("\n")

        row_data.clear()
    return True