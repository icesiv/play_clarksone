import json
import constant
import helpers

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def save_item():
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

def wait_for_page_to_load(page):
    page.wait_for_selector('body', timeout=350000)


def check_response(response, page):

    if "products.json" in response.url:
        resp = requests.get(response.url)

        if resp.status_code == 200:
            print("*" * 30)

            json_data = json.loads(
                resp.text.split('(', 1)[1].rsplit(')', 1)[0])

            product = json_data["Results"][0]

            product_name = product["Name"]
            product_image_url = product["ImageUrl"]
            product_upc = product["UPCs"]

            print("Name:", product_name)
            print("ImageUrl:", product_image_url)
            print("UPCs:", product_upc)

        else:
            print("got server code : " + str(resp.status_code))

        print("*" * 90)


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

def main():
     with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        # browser = p.chromium.launch()
        page = browser.new_page()
        # page.set_viewport_size({"width": 1280, "height": 1080})
        # page.route("**/*", helpers.block_aggressively)

        page = helpers.login(
            page, configs['USERNAME'], configs['PASSWORD']
        )
        # Now logged in

        # Load Items Link
        # links = (helpers.load_items('product_link',
        #                             constant.EXCEL_LIST_FILE_PATH))

        # for l in links:
        #     print(l)
        item_info = {}
        item_url = "/clarks-us/en_US/USD/c/Wallabee-/p/26155544"
        full_url = constant.BASE_URL + item_url

        page.goto(full_url)
        
        wait_for_page_to_load(page)
        print("Page loaded successfully!")
        
        html = page.inner_html("c-order_form_product_container_M")
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all product containers
        product_containers = soup.find_all('div', class_='c-order_form_product')

        for container in product_containers:
            # Extract data from each product container
            data_pc = container['data-pc']
            size = container.find('div', class_='c-order_form_product_size_digit').text
            price = container.find('div', class_='c-order_form_product_price_digit')['data-price']
            product_available = container.find('div', class_='c-order_form_product_available').text.strip()

            # Print the extracted information for each product
            print(f"data-pc: {data_pc}")
            print(f"Size: {size}")
            print(f"Price: {price}")
            print(f"Product Available: {product_available}")
            print("*" * 20)

        
        
        
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