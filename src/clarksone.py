import os
import sys
import json
import time
import random

from items_grab import Styles

import schedule
import constant

from items_grab import grab_items

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

def remain_time_text(rs):
    if(rs<1):
       return "00:00:00" 
    hours, remainder = divmod(rs, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

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

    user = configs['USERNAME'] 
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
# Listing Functions
# -----------------------------------------------------

def handle_listing(page, start_page, last_page, url, gender):
    for page_num in range(start_page, last_page+1):
        print("\n", "-"*20)
        print("Processing page", page_num)
        print("\n", "-"*20)
        
        list_url = url + str(page_num)
        html = load_list_page(page, list_url)
        
        if not html:
            continue
        
        if not parse_items(html, gender, page_num, page):
            break

def load_list_page(page, url):
    try:
        page.goto(url, timeout=280000)
        page.is_visible('div.product-tile')
        return page.inner_html('.product__listing-page')
    except:
        print("Error: Problem in URL. ",url)
        return None

def parse_items(html, gender, page_num,page):
    soup = BeautifulSoup(html, 'html.parser')
    product_tiles = soup.find_all(class_='product-tile')

    if len(product_tiles) < 1:
        return False

    styles_arr = []

    for product in product_tiles:
        title = product.find(class_='product-tile--name').text.strip()
        product_link = product.find(class_='product-tile--link')['href']
        sku = product.find(class_='product-tile--sku').text.strip()
        price = product.find(class_='product-tile--price').text.strip()

        price_div = product.find(class_='product-tile--price')
        if price_div is not None:
            msrp = price_div.text.strip()
        else:
            msrp = "-"
            
        s = Styles(sku)
        s.title = title
        s.link = product_link
        s.price = price
        s.msrp = msrp
        s.page_num = page_num
        s.gender = gender
       
        styles_arr.append(s)

    grab_items(styles_arr,page)
    return True

# -----------------------------------------------------
# Main Function
# -----------------------------------------------------

def start_scrap():
    start_time = time.time()
    print("\n\n")
    print("Starting .. ")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            # browser = p.chromium.launch(headless=False)
            # browser = p.chromium.launch()
        
            page = browser.new_page()
            page.set_viewport_size({"width": 1280, "height": 800})
            page.route("**/*", block_aggressively)
            
            page = login(page)

            # Steps Start
            
            # TODO Manage Continue / resume
            
            handle_listing(page, 1, 140, constant.get_url('woman_list_url'), "woman")

            handle_listing(page, 1, 47, constant.get_url('man_list_url'), "man")


            # Steps Done
            
            browser.close()
    
    except Exception as e:
        print(e)
        print("Error logged.")
        
    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)   
    print("\n\n\n\n")


# Starting Point ______________________________________
configs = load_config()

if __name__ == "__main__":
    start_scrap()
    print("-" * 40)
    
    s_delay = configs['SCHEDULE_DELAY'] * 60

    schedule.every(s_delay).minutes.do(start_scrap)

    while True:
        formatted_time = remain_time_text(schedule.idle_seconds())
        
        sys.stdout.write(f"\rNext call in {formatted_time}")
        sys.stdout.flush()
        
        schedule.run_pending()
        time.sleep(1)