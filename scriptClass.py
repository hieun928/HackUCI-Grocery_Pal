# ~~~~~~~~~~~~~~~~~~~~~`PYTHON 2.X~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
#PULLS ALL URL LINKS ON A SINGLE PAGE
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

circularFound = set();
for tag in tags:

    circular = re.compile('\/Circular.+');
   ## if (not tag == None) and tag.contains("Circular"):
        ##print tag.get('href')
    ret = str(tag.get('href'))
    if circular.match(ret):
        circularFound.add(ret)

for i in circularFound:
    print i

##AlbertsonsList = ['http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2',
##                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/2',
##                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/3',
##                  'http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2/4',
##                  
##
##
##




####Parses through a single web page for Title, Price, URL
##
##page = requests.get('http://albertsons.mywebgrocer.com/Circular/Irvine/2A6D73696/Weekly/2')
##
##
##soup = BeautifulSoup(page.content, 'html.parser')
###print soup.prettify()
##
##
##
####x = soup.find_all(class_="itemTitle")
##
##x = soup.find_all('div',class_="rightContent")
##y = soup.find_all('div',class_='leftContent')
##
##print len(x)
##for i in range(len(x)):
##    print 'Albertsons'
##    print x[i].find(class_="itemTitle").get_text()
##    print x[i].find(class_="itemPrice").get_text()
##    print y[i].find(class_= 'itemImage')['src']
##    print
##
