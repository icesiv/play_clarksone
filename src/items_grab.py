import sys 
import re
import constant
import helpers
import pandas as pd

from items import Item 

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def wait_for_page_to_load(page):
    page.wait_for_selector('body')

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
        
        feature_detail = ""
        for feature_name, feature_value in feature_details.items():
            feature_detail += (f"{feature_name}: {feature_value}; ")
            
        # Sole Material
        # Upper Material
        # Lining Material
        # Heel Height
        # Fastening
        # Boot Shaft Height 

        return feature_detail
    except:
        return "-"

def get_category(page):
    script_content = page.evaluate('''() => {
        const scriptTags = document.getElementsByTagName('script');
        for (const scriptTag of scriptTags) {
            if (scriptTag.type === 'text/javascript' && scriptTag.textContent.includes("'category': '")) {
                return scriptTag.textContent;
            }
        }
        return null;
    }''')

    category_match = re.search(r"'category': '([^']+)'", script_content)
    brand_match = re.search(r"'brand': '([^']+)'", script_content)

    if category_match:
        category = category_match.group(1)
        # print("Category:", category)
        
        category = category.replace("Fit,","")
        category = category.replace("Size,","")
        category = category.replace("Color,","")
    else:
        category = "-"
        # print("Category not found in JavaScript code.")

    if brand_match:
        brand = brand_match.group(1)
        # print("Brand:", brand)
    else:
        brand = "-"
        # print("Brand not found in JavaScript code.")
        
    return (category , brand)

def get_upc(page, key):
    items = []
    
    try:
        html = page.inner_html(key,timeout=3000)
    except:
        return items
    
    soup = BeautifulSoup(html, 'html.parser')
    product_containers = soup.find_all('div', class_='c-order_form_product')
    
    
    for container in product_containers:
        item = Item(container['data-pc'])
        try:
            item.size = container.find('div', class_='c-order_form_product_size_digit').text
            item.price = container.find('div', class_='c-order_form_product_price_digit')['data-price']
           
            availability_div = container.find('div', class_='c-order_form_product_available')
            product_available = availability_div.find('div', class_='c-order_form_product_availability_digit').get_text(strip=True)
            
            try:
                a = product_available.split("Next Available")
                item.available = a[0]
                item.available_next = a[1]
            except:
                item.available = product_available
                item.available_next = "-"
        except:
            print ("UPC Error: ",item.upc)
            continue
            
        items.append(item)
        
    return items
                    
def get_details(page, sku, title, msrp, link):
    # link = "/clarks-us/en_US/USD/c/Wallabee-/p/26155544"
    # link = "/clarks-us/en_US/USD/c/Cheyn-Zoe/p/26154389"
    # link = "/clarks-us/en_US/USD/c/Cielo-Charm/p/26171524"
    
    full_url = constant.BASE_URL + link
    page.goto(full_url, timeout=350000)
    wait_for_page_to_load(page)
    
    color = get_color(page.locator("div.product-name").text_content())
    feature_details = get_feature(page.inner_html("(//div[@class='pdp_details_tabs'])[1]"))
    images = get_images(sku) 
    
    itemsN = get_upc(page, "#c-order_form_product_container_N")
    itemsM = get_upc(page, "#c-order_form_product_container_M")
    itemsW = get_upc(page, "#c-order_form_product_container_W")
    
    category_n_brand = get_category(page)
    
    
    save_items(itemsN, sku, 'N', title, msrp, link,color,category_n_brand,feature_details,images)
    save_items(itemsM, sku, 'M', title, msrp, link,color,category_n_brand,feature_details,images)
    save_items(itemsW, sku, 'W', title, msrp, link,color,category_n_brand,feature_details,images)


def save_items(items: Item, sku, fit, title, msrp, link,color,category_n_brand,feature_details,images):
    if len(items) < 1:
        return
    
    for item in items:
        item.sku = sku
        item.title = title
        item.fit = fit
        
        item.msrp = msrp
        item.link = link
        item.color = color
        item.categorys = category_n_brand[0]
        item.brand = category_n_brand[1]
        item.feature_detail = feature_details
        
        item.image_1 = images[0]
        item.image_2 = images[1]
        item.image_3 = images[2]
        item.image_4 = images[3]
        item.image_5 = images[4]
        item.image_6 = images[5]
        item.image_7 = images[6]
            
        item.save_data()
            
def main():
     with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch()
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
            print("*" * 20)
            
            if index > 10:
                break
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