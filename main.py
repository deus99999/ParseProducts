import requests
from bs4 import BeautifulSoup
import json

OUT_FILE_NAME = 'out.json'
PAGES_COUNT = 10


def get_soup(page_url, **kwargs):
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
    else:
        soup = None
    return soup


def crowl_products(pages_count):
    urls = []
    fmt = "https://parsemachine.com/sandbox/catalog/?page={page}"
    for page_n in range(1, 1 + pages_count):
        print('page: {}'.format(page_n))
        page_url = fmt.format(page=page_n)
        soup = get_soup(page_url)

        if soup is None:
            break
        for tag in soup.select(".product-card .title"):
            href = tag.attrs['href']
            url = "https://parsemachine.com{}".format(href)
            urls.append(url)
    return urls


def format_int(s):
    s = s.split(".")
    for i in s:
        i = i.replace('\xa0', '')
    return int(i)


def parse_products(urls):
    data = []
    for url in urls:
        print('\tproduct: {}'.format(url))
        soup = get_soup(url)
        if soup is None:
            break
        name = soup.select_one('#product_name').text.strip()
        amount = format_int(soup.select_one('#product_amount').text)
        print(amount)
        techs = {}
        for row in soup.select('#characteristics tbody tr'):
            cols = row.select('td')
            cols = [c.text.strip() for c in cols]
            #print(row, cols)
            techs[cols[0]] = cols[1]
        #print(techs)

        item = {
            'name': name,
            'amount': amount,
            'techs': techs
        }

        data.append(item)
    return data


def main():
    urls = crowl_products(PAGES_COUNT)
    #print('\n'.join(urls))
    data = parse_products(urls)

    with open('OUT_FILE_NAME', 'a') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()

