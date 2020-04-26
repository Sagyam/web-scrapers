import concurrent.futures

from scraper import scrape

from tqdm import tqdm

import time


def start_thread(links):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
      result = list(tqdm(executor.map(scrape, links), total=len(links)))
    return result
