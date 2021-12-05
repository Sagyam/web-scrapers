# HamroBazar Scraper

Scrape data from HamroBazar

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
cd web-scrapers/HamroBazar
```

Install dependencies

```bash
pip install -r requirements.txt
```

Open setting.py to change value for **start_Id**, **stop_Id** and **min_post_count**

Start Scraping

```bash
python scrape.py
```
