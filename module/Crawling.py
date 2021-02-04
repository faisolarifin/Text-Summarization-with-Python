import requests
from bs4 import BeautifulSoup

class Crawling():
    def __init__(self, link):
        self.link = link
        
    def crawl(self):
        page = requests.get(self.link)
        soup = BeautifulSoup(page.content, 'html.parser')
        entry = soup.select('div.mw-parser-output p, div.mw-parser-output .mw-headline')
        result=''
        for i in entry:
            result += str(i.getText())
        return result