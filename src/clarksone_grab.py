from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import constant
import time
import random
from helpers import load_config

class Services:
    def __init__(self):
        self.configs = load_config()
        

    def block_aggressively(self, route): 
        if (route.request.resource_type in constant.RESOURCE_EXCLUSTIONS): 
            route.abort() 
        else: 
            route.continue_() 
    
    def check_response(self, response,page):
        if "page-fragment" in response.url:
            print("-" * 50)
            print("url: " , response)
            
            page.goto(response.url)
            page.is_visible('div.product-tile')
            html = page.inner_html('.product__listing-page')
            
            soup = BeautifulSoup (html, 'html.parser')
            product_tiles = soup.find_all(class_='product-tile')

            for product_tile in product_tiles:
                title = product_tile.find(class_='product-tile--name').text.strip()
                print("Product:", title)
                    
            print("-" * 50)
            

    def login(self): 
        with sync_playwright () as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            context = browser.new_context()
            page = context.new_page()
            
            page.set_viewport_size({"width": 1280, "height": 1080})
            page.route("**/*", self.block_aggressively) 
            page.on( "response" , lambda response: self.check_response(response,page))
            
            print("Starting .. ")
            print("-" * 50)
            
            page.goto(constant.get_url('login'))
            page.fill('input#j_username', self.configs['USERNAME'])
            page.fill('input#j_password', self.configs['PASSWORD'])
            page.click("button[type=submit]")
            
            page.wait_for_selector('div.carousel__component')
            random_seconds = random.uniform(1, 5)
            time.sleep(random_seconds)

            page.goto('https://us.clarksone.com/clarks-us/en_US/USD/Womens-All-Styles/c/w1')
            
            page.is_visible('div.product-tile')
            html = page.inner_html('.product__listing-page')
            # print(html)
            
            
            # SKU , Title , Cost , MSRP
            # Style ,UPC , Quantity Availability , 
            
            soup = BeautifulSoup (html, 'html.parser')
            product_tiles = soup.find_all(class_='product-tile')

            for product_tile in product_tiles:
                title = product_tile.find(class_='product-tile--name').text.strip()
                product_code = product_tile.find('a', {'name': True})['name']

                product_link = product_tile.find(class_='product-tile--link')['href']

                sku = product_tile.find(class_='product-tile--sku').text.strip()

                price = product_tile.find(class_='product-tile--price').text.strip()
                msrp = product_tile.find(class_='product-tile--price2').text.strip()

                color_options = [a['href'] for a in product_tile.select('.swatchVariant')]

                # Print the extracted information
                # print("Product Code:", product_code)
                # print("Title:", title)
                # print("Product Link:", product_link)
                # print("sku:", sku)
                # print("Price:", price)
                # print("MSRP:", msrp)
                # print("Color Options:", color_options)
                # print("*" * 20)
                # print("\n")
                
            # Scroll Down
            for x in range(1,5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                print("scrolling key press", x)
                time.sleep(1)
                
            random_seconds = random.uniform(1, 5)
            time.sleep(random_seconds)
            

            print("-" * 50)
            print("Done .. ")
            # browser. close()
        
    def main(self):
        self.login()
        
if __name__ == "__main__":
    a = Services()
    a.main()