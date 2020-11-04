import requests
from bs4 import BeautifulSoup
from requests.exceptions import InvalidSchema


def spider(base_url, path="", existing_pages=[]):
    pages = existing_pages
    if base_url not in pages:
        pages.append(base_url)
    links = []
    print(base_url + path)
    base_page = requests.get(base_url + path)
    soup = BeautifulSoup(base_page.text, "html.parser")

    elems = soup.find_all("a", href=True)
    for elem in elems:
        links.append(elem["href"])

    for link in links:

        if link.startswith("/"):
            page = base_url + link
        else:
            page = link

        if page in existing_pages:
            continue

        try:
            resp = requests.get(page)
        except InvalidSchema:
            continue

        if resp.ok:
            pages.append(page)
            print(page)
            spider(base_url, link, pages)

    return pages
