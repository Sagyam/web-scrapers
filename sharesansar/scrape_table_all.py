import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def scrape_table(data,date):

    # load data into bs4
    soup =BeautifulSoup(data, 'html.parser')
    # extract parts of  table from the page
    table = soup.find('table', { 'id': 'headFixed' })   
    # get the table headers
    headers = get_table_headers(table)
    # get all the rows of the table
    rows = get_table_rows(table)
    if len(rows) <2: 
        print("No record for ",date) 
        return 0
    # save table as csv file
    save_as_csv(headers, rows,date)

def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    return [th.text.strip() for th in table.find("tr").find_all("th")]

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        # grab all td tags in this table row
        tds = tr.find_all("td")
        cells = [td.text.strip() for td in tds]
        rows.append(cells)
    return rows

def save_as_csv(headers,rows,date):
    pd.DataFrame(rows, columns=headers).to_csv(f"{date}.csv",index=False)
    print(date,"Saved")
