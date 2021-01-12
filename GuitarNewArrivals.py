from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml
import numpy as np
from time import sleep
from random import randint
import csv

# session = HTMLSession()
# url = 'https://www.guitarcenter.com/New-Arrivals.gc?N=18144#pageName=collection-page&N=18144+46200&Nao=0&recsPerPage=30&postalCode=60126&radius=100&profileCountryCode=US&profileCurrencyCode=USD'



# def getdata(url):
#     req = session.get(url)
#     req.html.render(sleep=1)
#     soup = BeautifulSoup(req.html.html, 'html.parser')
#     return soup


NewArrivals = []
pages = np.arange(0, 330, 30)
for page in pages:
    url = "https://www.guitarcenter.com/New-Arrivals.gc?N=18144#pageName=collection-page&N=18144+46200&Nao=" + str(page) + "&recsPerPage=30&postalCode=60126&radius=100&profileCountryCode=US&profileCurrencyCode=USD"
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    print(url)

    # class="productGrid product-grid"
    arrivals = soup.findAll('li', {'class' : 'product-container'})
    # order = soup.findAll('div', {'class' : 'stickerText'})

    for guitar in arrivals:
        name = guitar.find('div', {'class': 'productTitle'}).text
        price = guitar.find('div', {'class': 'priceContainer mainPrice'}).text.replace('Your Price', '').strip()[:6]
        finance = getattr (guitar.find('div', {'class' : 'monthly-payments-details'}), 'text', None)
        order_type = guitar.find('span').text
        link = guitar.find('a')['href']

        # [tag.extract() for tag in guitar.find_all(class_='stars small rate-10 reviewCountGridLink')]
        guitar_new = {
        'Name' : name,
        'Price': price,
        'Order Type': order_type,
        'Financing' : finance,
        'Product Link': "https://www.guitarcenter.com" + link
            }
        NewArrivals.append(guitar_new)           


# soup = getdata(url)
# arrivals(soup)


df = pd.DataFrame(NewArrivals)
df = df.replace('\n','', regex=True)
df.to_csv('NewGuitar.csv', index=False)
print(df.head(100))

