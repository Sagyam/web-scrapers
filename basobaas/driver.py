import time
import os
from multithreading import start_thread

links = []
with open("urls.txt", 'r') as source_file:
    urls = source_file.readlines()
    for url in urls:
        links.append(url.strip())
        
start_thread(links)
