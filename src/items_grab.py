import sys 
import re
import constant

import constant
import pandas as pd

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class Styles():
    title = ""
    link = ""
    price = ""
    msrp = ""
    page_num = ""
    gender = ""
   
    def __init__(self, sku):
        self.sku = sku

class Item():
    upc = ""
    sku = ""
    title = ""
    link = ""
    fit = ""
    size = ""
    price = ""
    available = ""
    available_next = ""
    features = ""
    msrp = ""
    color  = ""
    categorys = ""
    brand = ""
    feature_detail = ""
    page_num = ""
    gender = ""
      
    image_1 = ""
    image_2 = ""
    image_3 = ""
    image_4 = ""
    image_5 = ""
    image_6 = ""
    image_7 = ""
    

    def __init__(self, upc):
        self.upc = upc
    pass

    def save_items_to_excel(self, data):
        new_df = pd.DataFrame(data)

        try:
            existing_df = pd.read_excel(constant.EXCEL_ITEMS_FILE_PATH)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except FileNotFoundError:
            combined_df = new_df

        combined_df.to_excel(constant.EXCEL_ITEMS_FILE_PATH, index=False)

    def save_data(self):
        data = {
            "UPC": [self.upc],
            "SKU": [self.sku],
            "Title": [self.title],
            "Fit": [self.fit],
            "Size": [self.size],
            "Price": [self.price],
            "Available": [self.available],
            "Available Next": [self.available_next],
            "Features": [self.features],
            "MSRP": [self.msrp],
            "Color": [self.color],
            "Categorys": [self.categorys],
            "Brand": [self.brand],
            "Feature Detail": [self.feature_detail],
            "Link": [self.link],
            "Gender": [self.gender],
            "List Page": [self.page_num],
            "Image 1": [self.image_1],
            "Image 2": [self.image_2],
            "Image 3": [self.image_3],
            "Image 4": [self.image_4],
            "Image 5": [self.image_5],
            "Image 6": [self.image_6],
            "Image 7": [self.image_7]
        }
    
        self.save_items_to_excel(data)
   
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
        html = page.inner_html(key,timeout=2000)
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
                    
def get_details(page, styles: Styles):
    full_url = constant.BASE_URL + styles.link
    print(">>>>" , full_url)
    
    page.goto(full_url, timeout=350000)
    page.wait_for_selector('body')
    
    color = get_color(page.locator("div.product-name").text_content())
    feature_details = get_feature(page.inner_html("(//div[@class='pdp_details_tabs'])[1]"))
    images = get_images(styles.sku) 
    
    itemsN = get_upc(page, "#c-order_form_product_container_N")
    itemsM = get_upc(page, "#c-order_form_product_container_M")
    itemsW = get_upc(page, "#c-order_form_product_container_W")
    itemsXW = get_upc(page, "#c-order_form_product_container_W")
    
    category_n_brand = get_category(page)
    
    save_items(itemsN, 'N', styles,color,category_n_brand,feature_details,images)
    save_items(itemsM, 'M', styles,color,category_n_brand,feature_details,images)
    save_items(itemsW, 'W', styles,color,category_n_brand,feature_details,images)
    save_items(itemsXW, 'XW', styles,color,category_n_brand,feature_details,images)


def save_items(items, fit, styles: Styles, color,category_n_brand,feature_details,images):
    if len(items) < 1:
        return
    
    for item in items:
        item.sku = styles.sku
        item.title = styles.title
        item.fit = fit
        
        item.page_num = styles.page_num
        item.gender = styles.gender
        
        item.msrp = styles.msrp
        item.link = styles.link
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
            
def grab_items(styles_arr, page):
    if page is None: 
        print("error login")
        sys.exit()

    for style in styles_arr:
        get_details(page, style)
        print("*" * 20)