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
        # page.route("**/*", helpers.block_aggressively)

        # page.set_viewport_size({"width": 1280, "height": 1080})
        # page.route("**/*", helpers.block_aggressively)

        page = helpers.login(
            page, configs['USERNAME'], configs['PASSWORD']
        )
        # Now logged in

        page.on('requestfinished', lambda request: handle_request(request))

        # Load Items Link
        # links = (helpers.load_items('product_link',
        #                             constant.EXCEL_LIST_FILE_PATH))

        # for l in links:
        #     print(l)
        item_info = {}
        item_url = "/clarks-us/en_US/USD/c/Stafford-Park5/p/20353216"
        full_url = constant.BASE_URL + item_url

        page.goto(full_url)
        
        
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        helpers.wait(30)

# https://api.bazaarvoice.com/data/products.json?passkey=aepj6ujftw8qdkioxfsc7k28s&apiversion=5.5&displaycode=19339-en_us&filter=id%3Aeq%3A26109039&limit=1&callback=bv_1111_19884
# https://us.clarksone.com/p/futureStocks?productCodes=261090393045,261090393050,261090393055,261090393060,261090393065,261090393070,261090393075,261090393085,261090393095,261090394025,261090394030,261090394035,261090394040,261090394045,261090394050,261090394055,261090394065,261090394075,261090394085,261090394095,261090395035,261090395040,261090395045,261090395050,261090395055,261090395060,261090395065,261090395070,261090395075,261090395085,261090395095,261090393045,261090393050,261090393055,261090393060,261090393065,261090393070,261090393075,261090393085,261090393095,261090394025,261090394030,261090394035,261090394040,261090394045,261090394050,261090394055,261090394065,261090394075,261090394085,261090394095,261090395035,261090395040,261090395045,261090395050,261090395055,261090395060,261090395065,261090395070,261090395075,261090395085,261090395095,



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