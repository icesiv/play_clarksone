RESOURCE_EXCLUSTIONS = ['image', 'stylesheet', 'media', 'font', 'other']

EXCEL_LIST_FILE_PATH = 'output_data/output_items_list.xlsx'
EXCEL_FILE_PATH = 'output_data/output_items_list.xlsx'

BASE_URL = "https://us.clarksone.com"


def get_url(key):

    if key == "login":
        return BASE_URL + "/clarks-us/en_US/USD/login"

    elif key == "woman_list_url":
        return BASE_URL + "/Womens-All-Styles/c/w1/page-fragment?q=:relevance&page="

    elif key == "man_list_url":
        return BASE_URL + "/All-Men\'s-Styles/c/m1/page-fragment?q=:relevance&page="

    else:
        return "Key Not Set"
