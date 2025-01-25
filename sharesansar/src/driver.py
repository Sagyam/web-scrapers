from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random
import os
import functools
from typing import List

from rich.progress import (
    Progress,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TextColumn,
    MofNCompleteColumn
)

from src.scrape_table import scrape_table
from src.settings import config, console, ConfigError
from src.return_dates import get_dates


def retry(max_attempts: int, initial_timeout: float, backoff_factor: float):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            timeout = initial_timeout
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    console.log(f"Error: {str(e)}")  # Log the exception
                    if attempts == max_attempts:
                        raise
                    console.log(f"Retry {attempts}/{max_attempts} after {timeout:.1f}s")
                    time.sleep(timeout)
                    timeout *= backoff_factor

        return wrapper

    return decorator

class ScraperMetrics:
    def __init__(self, total_days: int):
        self.total = total_days
        self.completed = 0
        self.start_time = time.time()
        self.times: List[float] = []

    def update(self, duration: float):
        self.completed += 1
        self.times.append(duration)
        if len(self.times) > config.retry_config['average_window']:
            self.times.pop(0)

    @property
    def average_duration(self) -> float:
        return sum(self.times) / len(self.times) if self.times else 0


def setup_driver() -> webdriver.Chrome:
    options = Options()
    if config.headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get("https://www.sharesansar.com/today-share-price")
    return browser


@retry(
    max_attempts=config.retry_config['attempts'],
    initial_timeout=config.retry_config['initial_timeout'],
    backoff_factor=config.retry_config['backoff_factor']
)
def process_day(day: str, driver: webdriver.Chrome, metrics: ScraperMetrics):
    start_time = time.time()
    try:
        # Random delay before starting (1-3 seconds)
        time.sleep(random.uniform(0.5, 1.5))

        # Wait for date input to be interactive
        date_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'fromdate'))
        )

        # Clear with staggered actions
        date_box.clear()
        time.sleep(random.uniform(0.2, 0.5))  # Human-like pause

        # Type date with artificial typing delay
        for char in day:
            date_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))

        # Randomized delay before submission
        time.sleep(random.uniform(0.5, 1.5))

        # Click submit with explicit wait
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btn_todayshareprice_submit'))
        )
        submit_button.click()

        # Wait for both table update AND previous data to clear
        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.ID, 'headFixed') and
                      "No Record Found" not in d.page_source
        )

        # Additional wait for data rows
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#headFixed tbody tr:not(.text-center)'))
        )

        # Randomized reading delay
        time.sleep(random.uniform(1, 2))

        html = driver.page_source
        scrape_table(data=html, date=day)

    except Exception as e:
        console.log(f"[red]Error processing {day}: {str(e)}[/red]")
        driver.get("https://www.sharesansar.com/today-share-price")
        raise

    finally:
        duration = time.time() - start_time
        metrics.update(duration)
        if duration > config.retry_config['slow_threshold']:
            console.log(f"[yellow]Slow scrape for {day} ({duration:.1f}s)[/yellow]")

        # Rate limit cooldown (3-7 seconds)
        time.sleep(random.uniform(3, 7))


def main():
    try:
        os.makedirs('../data', exist_ok=True)
        dates = get_dates(config.dates[0], config.dates[1])
        metrics = ScraperMetrics(total_days=len(dates))

        # Initialize a single WebDriver instance
        driver = setup_driver()

        with Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                MofNCompleteColumn(),
                TimeElapsedColumn(),
                TextColumn("ETA"),
                TimeRemainingColumn(),
                console=console
        ) as progress:
            task = progress.add_task("[cyan]Scraping...", total=len(dates))

            for day in dates:
                try:
                    process_day(day, driver, metrics)
                    progress.update(task, advance=1)
                except Exception as e:
                    console.log(f"[red]Failed {day}: {str(e)}[/red]")
                    # Refresh the page to ensure a clean state for the next day
                    driver.get("https://www.sharesansar.com/today-share-price")

        console.log(f"\n[green]Scraping completed![/green]")
        console.log(f"Average time per scrape: {metrics.average_duration:.1f}s")

    except ConfigError as e:
        console.log(f"[red]Configuration error: {str(e)}[/red]")
    except Exception as e:
        console.log(f"[red]Critical error: {str(e)}[/red]")
    finally:
        # Ensure the WebDriver is properly closed
        if 'driver' in locals():
            driver.quit()


if __name__ == "__main__":
    main()