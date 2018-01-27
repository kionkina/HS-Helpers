#venv -c "import amazonproduct"
# USER MUST PIP ISNTALL BeautifulSoup4
import requests
from bs4 import BeautifulSoup



def get_price(link):
    page = requests.get(link).text
    soup = BeautifulSoup(page, "html.parser")
    id="priceblock_ourprice"
    classs = "a-size-medium a-color-price"
    price = soup.find_all(['span', 'div'])
    return price


for i in get_price("https://www.amazon.com/Headphones-Otium-Waterproof-Sweatproof-Cancelling/dp/B018APC4LE/ref=sr_1_5?ie=UTF8&qid=1517035633&sr=8-5&keywords=headphones"):
    print i

