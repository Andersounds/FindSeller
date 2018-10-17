import requests
from bs4 import BeautifulSoup


class Page():
    def __init__(self,url,data):
        self.url = url
        self.order = data['_d']
        self.sortby = data['_s']
        self.pagenmbr = data['_p']
        self.parsedPage = None
        self.sellers = []
        self.prices = []
        self.getPageData()  # Läs in parsedpage på initialization

    def getPageData(self):
        page = requests.get(self.url)
        self.parsedPage = BeautifulSoup(page.text, 'html.parser')
        self.getSellersFromPageData()
        self.getPricesFromPageData()

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
            self.prices.append(float(pricestring))


#<button class="button buy add-to-cart" itemprop="price" content="20 SEK" data-control="add-to-cart" data-productid="7739398">20 SEK <i class="fa fa-shopping-cart"></i></button>

class bookObject():
    def __init__(self,_params):
        self.data = self._defaultDataFields()
        self._setChosenDataFields(_params)
        #self.maxprice = None
        #self.prio = None
        #self.no_of_sellers = None
        self.currentPage = None
        self.baseURL = 'https://www.bokborsen.se/'
        self.pages = [] #To be filled with objects of Page-type
    def __str__(self):
        return self.data['qt'] + '\t' + self.data['qa']

    def _defaultDataFields(self):
        data = {}
        data['q']  = '' #Generell sökning
        data['qa'] = '' #Author
        data['qt'] = '' #Title
        data['qi'] = '' #ISBN
        data['_s'] = 'price'    #Sort by
        data['_d'] = 'asc'      #Sorting order
        data['_p'] = '1'        #Page of search result
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
                'Order': '_d'}
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
            self.pages.append(Page(url,self.data)) # Add another page
            return 1


    #def help(self):


#class listOfBooks():
