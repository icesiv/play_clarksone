from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import helpers
import constant


class ListGrab:
    def __init__(self):
        self.configs = helpers.load_config()

    def main(self):
        with sync_playwright() as p:
            # browser = p.chromium.launch(headless=False, slow_mo=50)
            browser = p.chromium.launch()
            context = browser.new_context()

            page = context.new_page()
            # page.set_viewport_size({"width": 1280, "height": 1080})
            page.route("**/*", helpers.block_aggressively)

            page = helpers.login(
                page, self.configs['USERNAME'], self.configs['PASSWORD']
            )

            self.listing(page, 1, 140, constant.get_url(
                'woman_list_url'), "woman")

            self.listing(page, 1, 47, constant.get_url(
                'man_list_url'), "man")

    def listing(self, page, start_page, last_page, url, gender):
        for page_num in range(start_page, last_page+1):
            print("Processing page", page_num)

            list_url = url + str(page_num)

            html = self.load_list_page(page, list_url)
            if not self.parse_items(html, gender, page_num):
                break

    def load_list_page(self, page, url):
        page.goto(url)
        page.is_visible('div.product-tile')
        return page.inner_html('.product__listing-page')

    def parse_items(self, html, gender, page_num):
        soup = BeautifulSoup(html, 'html.parser')
        product_tiles = soup.find_all(class_='product-tile')

        if len(product_tiles) < 1:
            return False

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

            data = {
                "title": title,
                "product_link": product_link,
                "sku": sku,
                "price": price,
                "msrp": msrp,
                "list_page_num": page_num,
                "for": gender
            }

            data_arr.append(data)

        helpers.save_to_excel(data_arr)
        return True

# ________________________________________________________________________________


if __name__ == "__main__":
    start_time = helpers.current_time()

    print("Starting .. ")
    print("-" * 50)

    a = ListGrab()
    a.main()

    print("-" * 50)
    print("Done .. ")

    time_difference = helpers.current_time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)
