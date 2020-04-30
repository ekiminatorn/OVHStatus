from bs4 import BeautifulSoup

def strip(html):
    
    soup = BeautifulSoup(html, "html.parser")
    
    return soup.get_text()





