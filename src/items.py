from helpers import save_items_to_excel  

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
            "Image 1": [self.image_1],
            "Image 2": [self.image_2],
            "Image 3": [self.image_3],
            "Image 4": [self.image_4],
            "Image 5": [self.image_5],
            "Image 6": [self.image_6],
            "Image 7": [self.image_7]
        }
    
        save_items_to_excel(data)