import requests
from bs4 import BeautifulSoup

URL = 'https://jdihn.go.id/search/pusat?page='

def main():
    for i in range(1, 10, 1):
        res = requests.get("{}{}".format(URL, i))
        
        page = BeautifulSoup(res.text, 'html.parser')
        items = page.select('.item')
        for item in items:
            link = item.select('a')[1].get('href')
            print(link)
        break

if __name__ == "__main__":
    main()