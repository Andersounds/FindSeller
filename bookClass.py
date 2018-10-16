import urllib.request
import urllib.parse
#import beautifulsoup För att parsa upp informationen sen

class bookObject():
    def __init__(self,_params):
        self.data = self._defaultDataFields()
        self._setChosenDataFields(_params)
        self.maxprice = None
        self.prio = None
        self.no_of_sellers = None
        self.baseURL = 'https://www.bokborsen.se/?'
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
            else:
                print(key, ' is not an acceptable key.')

        return self.baseURL + urllib.parse.urlencode(self.data)



    #def help(self):


#class listOfBooks():
