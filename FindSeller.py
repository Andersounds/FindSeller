
#from lxml import html
import requests
from bs4 import BeautifulSoup

from bookClass import bookObject

def getListOfBooks():
    b1 = bookObject({'author':'Astrid','title':'pippi'})

#x = urllib.request.urlopen(url)
#print(x.read())


def main():
    b1 = bookObject({'author': 'astrid','title':'pippi'})
    url = b1.getURL({'page':1, 'order':'asc', 'sortby':'price'}) #example url
    print(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    sellers = soup.find_all(class_='seller')
    for item in sellers:
        seller = item.text.strip('Säljare:').strip()#strip initial 'Säljare:' and following whitespaces
        seller = seller.strip('(företag)').strip()  #strip trailing '(företag)' and trailing whitespaces
        print(seller)


main()
#Säljare:
#                                Riddare
