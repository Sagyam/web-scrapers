# Scraper
This scraper visits every url provided in url.txt if it is not not present visited_url.txt and scrapes data from pages of basobaas.com and saves it in csv format.

The script has tendency to crash for various reasons so script.sh will restart the script.It can quickly resume scraping in event of crash.

You can also select the no of threads in multithreading.py

Script also shows progress bar and prints the urls scraped.

For urls visit https://basobaas.com/sitemap.xml and use some  other tools to get urls in plain text format. 


# Usage
Inside multithreading.py select total no of threads (4 is default)

Run by python driver.py

## Run Locally

Clone the project

```bash
git clone https://github.com/Sagyam/web-scrapers.git
```

Install latest version of google-chrome and chromedriver for your OS [More Info](https://selenium-python.readthedocs.io/installation.html#drivers)

Create a virtual enviroment

```bash
virtualenv venv
```

Activate the virtual enviroment

**For Windows**

```bash
venv\Scripts\activate
```

**For Linux / OSX**

```bash
source venv/bin/activate
```

Go to the project directory

```bash
cd web-scrapers/basobaas
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Script

``` bash
python driver.py
```

