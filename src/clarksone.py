import os
import re
import sys
import json
import time
import random

import schedule
import constant

import pandas as pd

from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def load_config():
    try:
        with open(get_file(constant.CONFIG_PATH)) as f:
            config = json.load(f)
        
    except:
        print("Please create the config.json file.")
        sys.exit()

    return config

def get_file(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def wait(min , max =-1):
    if max == -1:
        max = min
    random_seconds = random.uniform(min, max)
    time.sleep(random_seconds)

def current_time_text():
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y %H-%M")
    return date_time

def block_aggressively(route):
    RESOURCE_EXCLUSTIONS = ['image', 'stylesheet', 'font']
    
    if (route.request.resource_type in RESOURCE_EXCLUSTIONS):
        route.abort()
    else:
        route.continue_()

# -----------------------------------------------------
# Login Function
# -----------------------------------------------------

def login(page):
    print("<" * 30)
    print("login process start")

    user = configs['USERNAME'], 
    password = configs['PASSWORD']
    
    try:
        page.goto(constant.get_url('login'), timeout=280000)
        page.fill('input#j_username', user)
        page.fill('input#j_password', password)
        page.click("button[type=submit]")
        page.wait_for_selector('div.carousel__component', timeout=280000)
        
        print("login success")
        print(">" * 30)
        
        return page
    except:
        print("login timeout..")
        return None
    
# -----------------------------------------------------
# Main Function
# -----------------------------------------------------

def start_scrap():
    start_time = time.time()
    print("Starting .. ")
    
    try:
        with sync_playwright() as p:
            # browser = p.chromium.launch(headless=False, slow_mo=50)
            # browser = p.chromium.launch(headless=False)
            browser = p.chromium.launch()
        
            page = browser.new_page()
            page.set_viewport_size({"width": 1280, "height": 800})
            page.route("**/*", block_aggressively)
            
            page = login(page)

            # Steps Start








            # Steps Done
            
            browser.close()
    
    except Exception as e:
        print(e)
        print("Error logged.")
        
    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)   
    print("\n\n\n\n")
# ________________________________________________________________________________

configs = load_config()

if __name__ == "__main__":
    start_scrap()
    print(f"Automatically Start Ordering in {configs['SCHEDULE_DELAY']} minutes")
    print("-" * 40)

    schedule.every(configs['SCHEDULE_DELAY']).minutes.do(start_scrap)

    while True:
        rs = schedule.idle_seconds()
        rm = rs // 60
        
        sys.stdout.write(f"\rNext call in {int(rm)}:{int(rs-(configs['SCHEDULE_DELAY']*rm))}")
        sys.stdout.flush()
        
        schedule.run_pending()
        time.sleep(1)