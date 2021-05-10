import requests
from bs4 import BeautifulSoup
import os

URL = 'https://jdihn.go.id/search/pusat?page='
DIRECTORY = 'downloads/'
PAGES = 6131

def main():
    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)

    for i in range(1, PAGES+1, 1):
        res = requests.get("{}{}".format(URL, i))
        
        page = BeautifulSoup(res.text, 'html.parser')
        items = page.select('.item')
        for item in items:
            link = item.select('a')[1].get('href')

            detail = requests.get(link)
            detail_page = BeautifulSoup(detail.text, 'html.parser')

            file_url = detail_page.select('embed')[0].get('src')

            file_binary = requests.get(file_url)
            
            file_name = file_url.split('/')[-1]
            with open(os.path.join(DIRECTORY, file_name), 'wb') as f:
                f.write(file_binary.content)
        break

if __name__ == "__main__":
    main()