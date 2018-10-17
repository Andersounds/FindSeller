#import requests
#from bs4 import BeautifulSoup
from bookClass import searchObject
from bookClass import compare

def getListOfBooks():
    pass


def main():
    searches = [searchObject({'author': 'murakami'}),
                searchObject({'author': 'arthur c clarke'}),
                searchObject({'author': 'aleksijevitj'}),
                searchObject({'title': 'Kom in på en öl och en smörgås'}),
                searchObject({'author': 'fallada'})]

    for search in searches:
        search.getAndCompileHits({'page':1, 'order':'asc', 'sortby':'price'},99)
    compare(searches)
#Bokgrottan har bra pris med omslag o skiva
#Måste ha ett sätt att spara undan alla träffar så att man enkelt kan utöka sökningen utan att behöva hämta all data igen

main()
