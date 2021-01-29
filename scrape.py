import requests
from bs4 import BeautifulSoup

page = requests.get('http://nj.hmart.com/shop/ramen-noodle/')


soup = BeautifulSoup(page.content, 'html.parser')
print soup.prettify()
