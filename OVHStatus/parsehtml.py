from bs4 import BeautifulSoup

def strip(html):
    
    soup = BeautifulSoup(html)
    
    return soup.get_text()





