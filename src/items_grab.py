import sys 
import json
import constant
import helpers
import pandas as pd

from items import Item 

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def wait_for_page_to_load(page):
    page.wait_for_selector('body')

def handle_request(request):
    # print(request.url)
    
    if "futureStocks?productCodes=" in request.url:
        print("futureStocks?productCodes=")
        print("*" * 90)
        r = request.response()
        print(r.text())
        print("*" * 90)

    if "products.json" in request.url:
        print("products.json")
        r = request.response()
        print("*" * 90)
        print(r.text())
        print("*" * 90)

def load_items():
    columns_to_read = ['title','product_link','sku','msrp']
    
    try:
        df = pd.read_excel(constant.EXCEL_FILE_PATH, usecols=columns_to_read)
        max_rows, max_cols = df.shape
        print(f'Total SKU: {max_rows}')
        if len(df) > 0:
            return df
        else:
            print("No Rows in the Excel file.")
            return None
        
    except Exception:
        print("Column not found in the Excel file.")
        return None
    
def get_color(c):
    try:
        c = c.replace("\n", "") 
        return c.split(" |")[0].strip()  
    except:
        return "-"
        
def get_images(sku):
    img_arr = []
    try:
        for i in range(1,8):
            img_arr.append(f"https://clarks.scene7.com/is/image/Pangaea2Build/{sku}_W_{i}?fmt=pjpg&wid=1024")
        return img_arr  
    except:
        return None
    
def get_feature(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')    

        product_details_tab = soup.find('div', class_='pdp_details_cmp_product_details_tab')
        feature_info_containers = product_details_tab.find_all('div', class_='pdp_details_cmp_product_details_tab_features_info')

        feature_details = {}
        for feature_info in feature_info_containers:
            feature_name = feature_info.find('div', class_='pdp_details_cmp_product_details_tab_feature_name').get_text(strip=True)
            feature_value = feature_info.find('div', class_='pdp_details_cmp_product_details_tab_feature_value').get_text(strip=True)
            feature_details[feature_name] = feature_value

        # Print the feature details
        # for feature_name, feature_value in feature_details.items():
        #     print(f"{feature_name}: {feature_value}")
        # Sole Material
        # Upper Material
        # Lining Material
        # Heel Height
        # Fastening
        # Boot Shaft Height 
        return feature_details
    except:
        return "-"

def get_upc(html):
    soup = BeautifulSoup(html, 'html.parser')
    size_elements = soup.find_all('div', class_='c-order_form_grid_body_input')

    for size_element in size_elements:
        # Extract size
        size = size_element.find('span', class_='c-order_form_grid_body_size_digit').text.strip()

        # Extract price
        price = size_element.find('input', type='number')['data-price']

        # Extract product availability
        availability = size_element.find('span', class_='c-order_form_grid_body_availability_digit').text.strip()

        print(f"Size: {size}, Price: ${price}, Availability: {availability}")


















    # soup = BeautifulSoup(html, 'html.parser')
    
    # .c-order_form_grid_body_entry
    
    # product_containers = soup.find_all('div', class_='c-order_form_product')
    
    # for container in product_containers:
    #     item = Item(container['data-pc'])
    #     item.size = container.find('div', class_='c-order_form_product_size_digit').text
    #     item.price = container.find('div', class_='c-order_form_product_price_digit')['data-price']
    #     print (item.upc , item.size)

    #     availability_div = container.find('div', class_='c-order_form_product_available')
    #     product_available = availability_div.find('div', class_='c-order_form_product_availability_digit').get_text(strip=True)
        
    #     try:
    #         a = product_available.split("Next Available")
    #         item.available = a[0]
    #         item.available_next = a[1]
    #     except:
    #         item.available = product_available
    #         item.available_next = "-"
        
        # print("item.available",item.available)
        # print("item.available_next",item.available_next)
    
    
    
    pass    
def get_details(page, sku, title, msrp, link):
    # link = "/clarks-us/en_US/USD/c/Wallabee-/p/26155544"
    # link = "/clarks-us/en_US/USD/c/Cheyn-Zoe/p/26154389"
    link = "/clarks-us/en_US/USD/c/Cielo-Charm/p/26171524"
    
    full_url = constant.BASE_URL + link
    page.goto(full_url, timeout=350000)
    wait_for_page_to_load(page)
    
    color = get_color(page.locator("div.product-name").text_content())
    feature_details = get_feature(page.inner_html("(//div[@class='pdp_details_tabs'])[1]"))
    images = get_images(sku) 
    
    # items = get_upc(page.inner_html("#c-order_form_product_container_M"))
    items = get_upc(page.inner_html(".c-order_form_grid"))
        
    # TODO : Save Items        
    print("*" * 20)
            
def main():
     with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 1080})
        page.route("**/*", helpers.block_aggressively)

        page = helpers.login(
            page, 
            configs['USERNAME'], 
            configs['PASSWORD']
        )
        
        if page is None: 
            print("error login")
            sys.exit()
       
        list_items = load_items()
        total = len(list_items)
        
        for index, row in list_items.iterrows():
            print(f"Getting Item {index+1} of {total}")
            get_details(page, row['sku'],row['title'],row['msrp'],row['product_link'])
            break
        

        sys.exit()
                
        print("--------------------------------------------------")
        helpers.wait(30)

# ________________________________________________________________________________

configs = helpers.load_config()

if __name__ == "__main__":
    start_time = helpers.current_time()

    print("Starting .. ")
    print("-" * 50)

    main()

    print("-" * 50)
    print("Done .. ")

    time_difference = helpers.current_time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)