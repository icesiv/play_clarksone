class Item():
    upc = ""
    size = ""
    price = ""
    available = ""
    available_next = ""
    features = ""

    def __init__(self, sku, title, product_link):
        self.sku = sku
        self.title = title
        self.link = product_link
    pass