# Scraper
This scraper visits every url provided in url.txt if it is not not present visited_url.txt and scrapes data from pages of basobaas.com and saves it in csv format.

The script has tendency to crash for various reasons so script.sh will restart the script.It can quickly resume scraping in event of crash.

You can also select the no of threads in multithreading.py

Script also shows progress bar and prints the urls scraped.

For urls visit https://basobaas.com/sitemap.xml and use some  other tools to get urls in plain text format. 

# Requirements
pip install beautifulsoup4

pip install selenium

pip install tqdm


# Usage
Inside multithreading.py select total no of threads (4 is default)

Run by python driver.py

