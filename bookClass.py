import requests
from bs4 import BeautifulSoup
import time # to not make too many requests too fast

#Möjliga approaches:
#   1. -För varje bokobjekt, läs in alla säljare som har den i lager, och respektive pris
#      - Kolla sedan uttömmande om en säljare av en bok återfinns i någon annan säljarlista

#   2. -För varje bokobjekt av prio 1, läs in alla säljare som har den i lager
#      -För varje säljare som har bok av prio 1 i lager, sök om den även har ngn annan önskebok i lager
class Page():
    def __init__(self,url,data):
        self.url = url
        self.order = data['_d']
        self.sortby = data['_s']
        self.pagenmbr = data['_p']
        self.parsedPage = None
        self.sellers = []
        self.authors = []
        self.titles = []
        self.prices = []
        self.getPageData()  # Läs in parsedpage på initialization

    def getPageData(self):
        page = requests.get(self.url)
        self.parsedPage = BeautifulSoup(page.text, 'html.parser')
        self.getSellersFromPageData()
        self.getPricesFromPageData()
        self.getTitlesAndAuthorsFromPageData()
        self.parsedPage = 0#free space?
    def getSellersFromPageData(self):
        sellers = self.parsedPage.find_all(class_='seller')
        for item in sellers:
            seller = item.text.strip('Säljare:').strip()#strip initial 'Säljare:' and following whitespaces
            seller = seller.strip('(företag)').strip()  #strip trailing '(företag)' and trailing whitespaces
            self.sellers.append(seller)
    def getPricesFromPageData(self):
        prices = self.parsedPage.find_all(class_='button buy add-to-cart')
        #prices = self.parsedPage.find_all('button',"35 SEK")
        #prices = self.parsedPage.find_all(content=True)
        for item in prices:
            pricestring = str(item.text).strip(' SEK')
            self.prices.append(pricestring)#Obs prices as strings
    def getTitlesAndAuthorsFromPageData(self):
        titles = self.parsedPage.find_all(itemprop = 'name')
        i = 0# used to only take every second item
        for item in titles:
            if i==0:
                self.titles.append(str(item.text)) #First is book title
                i = 1
            elif i == 1:
                self.authors.append(str(item.text)) #Second is autor
                i = 0

class searchObject():
    def __init__(self,_params):
        self.data = self._defaultDataFields()
        self._setChosenDataFields(_params)
        #self.maxprice = None
        #self.prio = None
        #self.no_of_sellers = None
        self.currentPage = None
        self.baseURL = 'https://www.bokborsen.se/'
        self.pages = [] #To be filled with objects of Page-type
        self.dictOfSellers = {} #seller is key, value is number of hits on search
    def __str__(self):
        return 'Title:\t' + self.data['qt'] + '\n' + 'Author:\t' + self.data['qa'] + '\n' + 'Seller:\t' + self.data['qs'] + '\n' + 'ISBN:\t' + self.data['qi']
    def _defaultDataFields(self):
        data = {}
        data['q']  = '' #Generell sökning
        data['qa'] = '' #Author
        data['qt'] = '' #Title
        data['qi'] = '' #ISBN
        data['_s'] = 'price'    #Sort by
        data['_d'] = 'asc'      #Sorting order
        data['_p'] = '1'        #Page of search result
        data['qs'] = ''         #Seller
        data['g'] = '0' #dont know but i think necessary
        data['c'] = '0' #dont know but i think necessary
        data['f'] = '1' #dont know but i think necessary
        data['fi'] = '' #dont know
        data['fd'] = '' #dont know
        return data
    def _setChosenDataFields(self,givenKeys):
        acceptedKeys = {'author': 'qa',     #Relate readable keys with url keys
                'Author': 'qa',
                'title': 'qt',
                'Title': 'qt',
                'isbn': 'qi',
                'ISBN': 'qi',
                'sortby': '_s',
                'Sortby': '_s',
                'order': '_d',
                'Order': '_d',
                'Seller': 'qs',
                'seller': 'qs'}
        for key in givenKeys:         # Iterate through all keys given
            if key in acceptedKeys:   # If input is in the dict of accepted inputs
                self.data[acceptedKeys[key]] = givenKeys[key]
            else:
                print(key, ' is not an acceptable key.')
    def add(self,givenKeys): # Add or change
        _setChosenDataFields(givenKeys)
    def encodeurl(self): #Takes the dict in self.data and parses a url string together with self.baseURL
        trailingurl = '?'
        for key in self.data:
            trailingurl = trailingurl + key + '=' + self.data[key] + '&'
        return self.baseURL + trailingurl
    def getURL(self,parameters): #Creates an url that shows the result of a search of all set tags, sorted by what is set or default, and shows result page that is set
        # Only use keys that are not '' ? check if works!
        acceptedKeys = {'page':'_p',
                        'Page':'_p',
                        'sortby':'_s',
                        'Sortby':'_s',
                        'order': '_d',
                        'Order': '_d'}
        acceptedTags = {'_s': ['created_at','title','author','price'],
                        '_d': ['asc','desc']}

        for key in parameters:
            if key in acceptedKeys:
                if acceptedKeys[key] in acceptedTags: #If tag can only be one of finite defined statements
                    if parameters[key] in acceptedTags[acceptedKeys[key]]:
                        self.data[acceptedKeys[key]] = str(parameters[key]) # Make string so that page can be given as number
                    else:
                        print(parameters[key], 'is not an acceptable tag for key', key)
                        print('Key', key, 'accepts the following tags: ', acceptedTags[acceptedKeys[key]])
                else: # if tag is accepted but can be anything (ie if tag is page number)
                    self.data[acceptedKeys[key]] = str(parameters[key])
            else:
                print(key, ' is not an acceptable key.')
        self.currentPage = self.data['_p']  #Set current page of url so we can keep track
        return self.encodeurl()
    def addPage(self,url): #If return 1 page is added, if return 0, there are no more results
        if len(self.pages)>0:   #If there are already some results
            if len(self.pages[-1].sellers) > 0: # if last page has sellers in it
                self.pages.append(Page(url,self.data)) # Add another page
                return 1
            else:                                       #If last page is empty
                return 0                                #no more pages
        else:                                           #If there are no pages yet, add the first one
            self.pages.append(Page(url,self.data)) # Add first page
            return 1
    def addAllPages(self,initurl,lastpage):
        print('Adding all pages from search')
        url = initurl
        nextpage = int(self.data['_p'])
        while(self.addPage(url) and nextpage<=lastpage):
            print('Got page ' + self.data['_p'])
            nextpage += 1
            url = self.getURL({'page':nextpage})# Get url for next page
            time.sleep(0.2)
    def compileSellers(self): #create dictOfSellers where every seller can be
        for page in self.pages:
            for seller in page.sellers:
                if not seller in self.dictOfSellers:
                    self.dictOfSellers[seller] = 1
                else:
                    self.dictOfSellers[seller] += 1
    def printSellers(self):
        print('Antal \tFörsäljare')
        for item in self.dictOfSellers:
            print(str(self.dictOfSellers[item])+ '\t' + item)
    def getAndCompileHits(self,data,lastpage):
        url = self.getURL(data)
        self.addAllPages(url,lastpage)
        self.compileSellers()
        #self.printSellers()

def compare(listofsearchobjects):
    n = len(listofsearchobjects)
    dictOfHits = {}
    for i in range(n):
        for seller in listofsearchobjects[i].dictOfSellers:
            for j in range(n):
                if not i==j:
                    if seller in listofsearchobjects[j].dictOfSellers:
                        if not seller in dictOfHits:
                            dictOfHits[seller] = searchHit(seller,i,j)
    for i in dictOfHits:
        print(dictOfHits[i])
#key: no_of_hits
#data: [seller,[hitsearch1, hitsearch2, ...]]

class searchHit():
    def __init__(self,seller,i,j):
        self.seller = seller
        self.hits = []
        if not i in self.hits:
            self.hits.append(i)
        if not j in self.hits:
            self.hits.append(j)
    def __str__(self):
        return str(self.hits) + '\t' + self.seller
#class possibleSeller():# An object that contains a seller and the search hits that he or she has in stock
#    def __init__(self):


    #def help(self):
