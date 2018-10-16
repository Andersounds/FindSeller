
import urllib.request
import urllib.parse

from bookClass import bookObject

def getListOfBooks():
    b1 = bookObject({'author':'Astrid','title':'pippi'})

#x = urllib.request.urlopen(url)
#print(x.read())


def main():
    b1 = bookObject({'author': 'astrid','title':'pippi'})
    url = b1.getURL({'page':1, 'order':'asc', 'sortby':'price'}) #example url
    print(url)
main()
