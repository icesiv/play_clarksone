import json
import os
import time
import random

import constant
import pandas as pd


def login(page, user, password):
    print("<" * 30)
    print("login process start")
    
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

def get_file(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def load_config():
    with open(get_file('../config.json')) as f:
        return json.load(f)

def wait(min, max = 1):
    if min > max:
        max = min
        
    random_seconds = random.uniform(1, max)
    time.sleep(random_seconds)

def current_time():
    return time.time()

def block_aggressively(route):
    if (route.request.resource_type in constant.RESOURCE_EXCLUSTIONS):
        # print("XXX -->" ,route.request.url)
        route.abort()
    else:
        route.continue_()


def save_to_excel(new_data):
    new_df = pd.DataFrame(new_data)

    try:
        existing_df = pd.read_excel(constant.EXCEL_FILE_PATH)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    except FileNotFoundError:
        combined_df = new_df

    combined_df.to_excel(constant.EXCEL_FILE_PATH, index=False)

    print(
        f'Data has been appended to {constant.EXCEL_FILE_PATH}')
    
def save_items_to_excel(data):
    new_df = pd.DataFrame(data)

    try:
        existing_df = pd.read_excel(constant.EXCEL_ITEMS_FILE_PATH)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    except FileNotFoundError:
        combined_df = new_df

    combined_df.to_excel(constant.EXCEL_ITEMS_FILE_PATH, index=False)

    print(
        f'Data has been appended to {constant.EXCEL_ITEMS_FILE_PATH}')

