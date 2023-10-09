import constant
import helpers
from bs4 import BeautifulSoup
import json
import helpers

import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False, slow_mo=50)
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.route("**/*", helpers.block_aggressively)

        # await page.set_viewport_size({"width": 1280, "height": 1080})
        # page.route("**/*", helpers.block_aggressively)

        # login page
        print("<" * 30)
        print("login process start")
        await page.goto(constant.get_url('login'))
        await page.fill('input#j_username', configs['USERNAME'])
        await page.fill('input#j_password', configs['PASSWORD'])
        await page.click("button[type=submit]")

        await page.wait_for_selector('div.carousel__component')
        print("login success")
        print(">" * 30)
        # Now logged in

        page.on('requestfinished', lambda request: handle_request(request))

        # Load Items Link
        # links = (helpers.load_items('product_link',
        #                             constant.EXCEL_LIST_FILE_PATH))

        # for l in links:
        #     print(l)
        item_info = {}
        item_url = "/clarks-us/en_US/USD/c/Nalle-Lace/p/26163570"
        full_url = constant.BASE_URL + item_url

        await page.goto(full_url)

# https://api.bazaarvoice.com/data/products.json?passkey=aepj6ujftw8qdkioxfsc7k28s&apiversion=5.5&displaycode=19339-en_us&filter=id%3Aeq%3A26109039&limit=1&callback=bv_1111_19884
# https://us.clarksone.com/p/futureStocks?productCodes=261090393045,261090393050,261090393055,261090393060,261090393065,261090393070,261090393075,261090393085,261090393095,261090394025,261090394030,261090394035,261090394040,261090394045,261090394050,261090394055,261090394065,261090394075,261090394085,261090394095,261090395035,261090395040,261090395045,261090395050,261090395055,261090395060,261090395065,261090395070,261090395075,261090395085,261090395095,261090393045,261090393050,261090393055,261090393060,261090393065,261090393070,261090393075,261090393085,261090393095,261090394025,261090394030,261090394035,261090394040,261090394045,261090394050,261090394055,261090394065,261090394075,261090394085,261090394095,261090395035,261090395040,261090395045,261090395050,261090395055,261090395060,261090395065,261090395070,261090395075,261090395085,261090395095,


async def handle_request(request):
    if "futureStocks?productCodes=" in request.url:
        print("futureStocks?productCodes=")
        print("*" * 90)
        r = await request.response()
        print(await r.text())
        print("*" * 90)

    if "products.json" in request.url:
        print("products.json")
        r = await request.response()
        print("*" * 90)
        print(await r.text())
        print("*" * 90)


async def save_item():
    if "futureStocks?productCodes=" in request.url:
        print("futureStocks?productCodes=")
        print("*" * 90)
        r = await request.response()
        print(await r.text())
        print("*" * 90)

    if "products.json" in request.url:
        print("products.json")
        r = await request.response()
        print("*" * 90)
        print(await r.text())
        print("*" * 90)


async def check_response(response, page):

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


# ________________________________________________________________________________


configs = helpers.load_config()

if __name__ == "__main__":
    start_time = helpers.current_time()

    print("Starting .. ")
    print("-" * 50)

    asyncio.run(main())

    print("-" * 50)
    print("Done .. ")

    time_difference = helpers.current_time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)
