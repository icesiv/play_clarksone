import os
import time
import random
import pandas as pd

import constant

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from helpers import load_config



def wait(max):
    random_seconds = random.uniform(1, max)
    time.sleep(random_seconds)  

class Services:
    def __init__(self):
        self.configs = load_config()       
        
    def main(self):
        with sync_playwright () as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            context = browser.new_context()
            
            page = context.new_page()
            page.set_viewport_size({"width": 1280, "height": 1080})
            page.route("**/*", self.block_aggressively) 
            # page.on( "response" , lambda response: self.check_response(response,page))
            
            page = self.login(page)
            wait(5)

            # woman_list_url = "https://us.clarksone.com/clarks-us/en_US/USD/Womens-All-Styles/c/w1"
            # html = self.load_list_page(page, woman_list_url)
            # self.parse_items(html)
            
                
            page_num = 24
            woman_list_url = f"https://us.clarksone.com/Womens-All-Styles/c/w1/page-fragment?q=:relevance&page={page_num}"
            
            html = self.load_list_page(page, woman_list_url)
            self.parse_items(html)

            # # # Scroll Down
            # for x in range(1,5):
            #     page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            #     print("scrolling key press", x)
            #     time.sleep(2)
            
            # browser.close()
            
    def load_list_page(self, page, url):
        page.goto(url)
        page.is_visible('div.product-tile')
        return page.inner_html('.product__listing-page')
            
    def parse_items(self, html):
        soup = BeautifulSoup (html, 'html.parser')
        product_tiles = soup.find_all(class_='product-tile')
        
        print(len(product_tiles))
        
        data_arr = []

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
            
            # SKU , Title , Cost , MSRP
            
            data = {
                    "title" : title,
                    "product_link" : product_link,
                    "sku" : sku,
                    "price" : price,
                    "msrp" : msrp
            }
            
            data_arr.append(data)
            
        self.save_to_excel(data_arr)
            

    def save_to_excel(self, data):
        df = pd.DataFrame(data)
        if os.path.exists(constant.EXCEL_FILE_PATH):
            df.to_excel(constant.EXCEL_FILE_PATH, index=True)
        else:
            writer = pd.ExcelWriter(constant.EXCEL_FILE_PATH)
            existing_df = pd.read_excel(constant.EXCEL_FILE_PATH)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_excel(constant.EXCEL_FILE_PATH, index=False)
            writer.close()
        

            
    def block_aggressively(self, route): 
        if (route.request.resource_type in constant.RESOURCE_EXCLUSTIONS): 
            route.abort() 
        else: 
            route.continue_() 
    
    def check_response(self, response,page):
        print(response.url)
        # if "page-fragment" in response.url:
        #     print("-" * 50)
        #     print("url: " , response)
            
        #     page.goto(response.url)
        #     page.is_visible('div.product-tile')
        #     html = page.inner_html('.product__listing-page')
            
        #     soup = BeautifulSoup (html, 'html.parser')
        #     product_tiles = soup.find_all(class_='product-tile')

        #     for product_tile in product_tiles:
        #         title = product_tile.find(class_='product-tile--name').text.strip()
        #         print("Product" : title)
                    
        #     print("-" * 50)
            
    def login(self,page): 
        page.goto(constant.get_url('login'))
        page.fill('input#j_username', self.configs['USERNAME'])
        page.fill('input#j_password', self.configs['PASSWORD'])
        page.click("button[type=submit]")
        
        page.wait_for_selector('div.carousel__component')
        return page
          
# ________________________________________________________________________________

if __name__ == "__main__":
    start_time = time. time()
    
    print("Starting .. ")
    print("-" * 50)
    
    a = Services()
    a.main()
    
    print("-" * 50)
    print("Done .. ")
    
    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)