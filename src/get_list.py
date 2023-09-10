import requests

url = "https://us.clarksone.com/Womens-All-Styles/c/w1/page-fragment"

querystring = {"q":":relevance","page":"2"}

payload = ""
headers = {
    "cookie": "anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; cmTPSet=Y; CoreID6=30603330019316930321950&ci=90375373; BVBRANDID=ddd5a276-3fff-4c52-a806-334f26c47a83; CMAVID=none; BVImplmain_site=19339; BVBRANDSID=564c2d80-e1bf-41b5-8606-c0a51de2dfdb; acceleratorSecureGUID=efd9122462edd3fbb5cf448187abf2deae6480cb; JSESSIONID=Y1-29fdb576-f09a-436a-99dc-ff6a0d4d8ffa; AWSALB=5L/ep+3GHSGwVae0vUNwDeknFI9C3KIpynpKOAKw9WCap7JYMWwdZqqG7gA1IGUcwigYbE8jPpj8ctTEqe5URrSb1tYX9qebfOzW+L18ppwdBPDCxaEm/qigl7mm; AWSALBCORS=5L/ep+3GHSGwVae0vUNwDeknFI9C3KIpynpKOAKw9WCap7JYMWwdZqqG7gA1IGUcwigYbE8jPpj8ctTEqe5URrSb1tYX9qebfOzW+L18ppwdBPDCxaEm/qigl7mm; 90375373_clogin=v=1&l=54875611694244480857&e=1694246308118",
    "authority": "us.clarksone.com",
    "accept": "*/*",
    "accept-language": "en-BD,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "referer": "https://us.clarksone.com/clarks-us/en_US/USD/Womens-All-Styles/c/w1",
    "sec-ch-ua": "'Chromium';v='116', 'Not)A;Brand';v='24', 'Google Chrome';v='116'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)