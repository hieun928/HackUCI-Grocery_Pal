import requests
from bs4 import BeautifulSoup
import re
import urllib2
from collections import namedtuple
import queue



albertsons_prefix = 'http://albertsons.mywebgrocer.com'
all_key_regex = re.compile('\/Circular.+')

pav_prefix = 'http://pavilions.safeway.com'
vons_prefix = 'http://vons.safeway.com'

VonsList = ['http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/2',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/3',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/4',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/5',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/6',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/7',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/8',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/9',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/10',
            ]

PavilionsList = ['http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/1',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/2',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/3',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/4',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/5',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/6',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/7',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/8',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/9',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/10',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/11',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/12',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/13',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/14',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/15'
                 ]

AlbertsonsList = ['http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/2',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/3',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/4',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/5',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/6',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/7',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/8',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/9',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/10'
                  ]


Item = namedtuple('Item', 'Store Title Price URL')

PARSER = 'lxml'
AlbertsonsItems = []
VonsItems = []
PavilionsItems = []
class LinkedPage:

    def __init__(self, page, items,  prefix, key_regex=all_key_regex):

        self.page = requests.get(page);
        self.soup = BeautifulSoup(self.page.content)
        self.linked = set();
        self.add_items(items, prefix);
        #self.get_linked(prefix, key_regex)

    def add_items(self, items, prefix):

        x = self.soup.find_all(class_="itemTitle")
        x = self.soup.find_all('div',class_="rightContent")
        y = self.soup.find_all('div',class_='leftContent')
        for k in range(len(x)):

            title = x[k].find(class_="itemTitle").get_text()
            price = x[k].find(class_="itemPrice").get_text()
            img = y[k].find(class_= 'itemImage')['src']
            items.append(Item(prefix, title, price, img))

    def get_linked(self, prefix, key_regex):
        tags = self.soup.find_all('a')


        # Extracting URLs from the attribute href in the <a> tags.

        Found = set()
        for tag in tags:


           ## if (not tag == None) and tag.contains("Circular"):
                ##print tag.get('href')
            ret = str(tag.get('href'))
            if key_regex.match(ret):

                Found.add(prefix + ret)

        self.linked = Found


AlbertsonSet = set()
cachedPages = {'Albertsons' : []}

def getLinks(start, store, items, lst, prefix):
    explored = set()
    explored.add(start)
    q = queue.Queue()
    q.put(start)
    while not qw.empty():

        page = q.get()

        lp = LinkedPage(page, items, prefix)
        cachedPages[store].append(lp)
        for link in lp.linked:
            if link not in explored:
                q.put(link)
                explored.add(link)


def writeTuple(fil, lst):

    write_stream = open(fil, 'w')
    for tup in lst:
        write_stream.write(tup.Title + ',' + tup.Price + ','+ tup.URL + '\n')
    write_stream.close()

AlbertsonsStart = "http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2"
FullCrawl = False
if FullCrawl:
    getLinks(AlbertsonsStart, 'Albertsons', AlbertsonsItems, AlbertsonsList, albertsons_prefix)
else:
    for page in AlbertsonsList:
        LinkedPage(page, AlbertsonsItems, albertsons_prefix)
    for page in VonsList:
        LinkedPage(page,  VonsItems, vons_prefix)
    for page in PavilionsList:
        LinkedPage(page, PavilionsItems, pav_prefix)
writeTuple('Albertsons',AlbertsonsItems)
writeTuple('Vons', VonsItems)
writeTuple('Pavilions', PavilionsItems)




Item = namedtuple('Item', 'Store Title Price URL')



'''import requests
from bs4 import BeautifulSoup
import re
import urllib2

AlbertsonsList = ['http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/2',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/3',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/4',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/5',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/6',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/7',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/8',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/9',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/10'
                  ]


Item = namedtuple('Item', 'Store Title Price URL')

PARSER = 'lxml'
AlbertsonItems = []
class LinkedPage:
    prefix = 'http://albertsons.mywebgrocer.com'
    key_regex = re.compile('\/Circular.+')
    def __init__(self, page, items=AlbertsonItems):

        self.page = requests.get(page);
        self.soup = BeautifulSoup(self.page.content)
        self.linked = set();
        self.add_items(items);


    def add_items(self, items):

        x = self.soup.find_all(class_="itemTitle")
        x = self.soup.find_all('div',class_="rightContent")
        y = self.soup.find_all('div',class_='leftContent')
        for k in range(len(x)):

            title = x[k].find(class_="itemTitle").get_text()
            price = x[k].find(class_="itemPrice").get_text()
            img = y[k].find(class_= 'itemImage')['src']
            print prefix
            print title
            print price
            print img
            print 'Item ', count
            print
            items.append(Item(prefix, title, price, img))

    def get_linked(self):
        tags = self.soup.find_all('a')


        # Extracting URLs from the attribute href in the <a> tags.

        Found = set()
        for tag in tags:


           ## if (not tag == None) and tag.contains("Circular"):
                ##print tag.get('href')
            ret = str(tag.get('href'))
            if LinkedPage.key_regex.match(ret):
                Found.add(ret)

        for i in Found:
            print i
        self.linked = Found


AlbertsonSet = set()
cachedPages = {'Albertsons' : []}

def getLinks_r(start, explored, store, wrapper):
    if start in explored:
        return
    explored.add(start)
    linkedp = wrapper(start)
    cachedPages[store].append(linkedp)
    linkedp.get_linked()

    for page in linkedp.linked:
        explored.add(wrapper.prefix + page)
        getLinks_r(wrapper.prefix + page, explored, store, wrapper)

AlbertsonsStart = "http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2"
getLinks_r(AlbertsonsStart, AlbertsonSet, 'Albertsons', LinkedPage)
print AlbertsonSet


#########################  SCRAPE EVERYTHING   ###################################
import requests
from bs4 import BeautifulSoup
import re
import urllib2
from collections import namedtuple

#~~~~~~~~~~~~~~~~~~~~PULLS ALL URL LINKS ON A SINGLE PAGE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
url = "http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2"

# Getting the webpage, creating a Response object.
response = requests.get(url)

# Extracting the source code of the page.
data = response.text

# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
soup = BeautifulSoup(data, 'lxml')

# Extracting all the <a> tags into a list.
tags = soup.find_all('a')

# Extracting URLs from the attribute href in the <a> tags.

##circularFound = set();
##for tag in tags:
##
##    circular = re.compile('\/Circular.+');
##   ## if (not tag == None) and tag.contains("Circular"):
##        ##print tag.get('href')
##    ret = str(tag.get('href'))
##    if circular.match(ret):
##        circularFound.add(ret)
##
##for i in circularFound:
##    print i

AlbertsonsList = ['http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/2',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/3',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/4',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/5',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/6',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/7',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/8',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/9',
                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/10',
                  ]

VonsList = ['http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/2',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/3',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/4',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/5',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/6',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/7',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/8',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/9',
            'http://vons.safeway.com/Circular/Santa-Ana-3650-S-Bristol-St-/1D4775157/Weekly/2/10',
            ]

PavilionsList = ['http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/1',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/2',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/3',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/4',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/5',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/6',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/7',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/8',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/9',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/10',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/11',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/12',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/13',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/14',
                 'http://pavilions.safeway.com/Circular/Newport-Coast-21181-Newport-Coast-Dr-/15CC74007/Weekly/2/15'
                 ]


Item = namedtuple('Item', 'Store Title Price URL')

AlbertsonsItemList = []
VonsItemList = []
PavilionsItemList = []

#if __name__ == '__main__':


##Parses through a single web page for Title, Price, URL
# i is the index, j is the url
count = 0
for i, j in enumerate(PavilionsList):
    page = requests.get(j)
    print 'item',i

    soup = BeautifulSoup(page.content, 'html.parser')
    #print soup.prettify()

    x = soup.find_all(class_="itemTitle")
    x = soup.find_all('div',class_="rightContent")
    y = soup.find_all('div',class_='leftContent')

    for k in range(len(x)):

        title = x[k].find(class_="itemTitle").get_text()
        price = x[k].find(class_="itemPrice").get_text()
        img = y[k].find(class_= 'itemImage')['src']
        print 'Pavilions'
        print title
        print price
        print img
        print 'Item ', count
        print
        PavilionsItemList.append(Item('Pavilions', title, price, img))
        count+=1

for i in PavilionsItemList:
    print i
    '''
