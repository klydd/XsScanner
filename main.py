from scanner import scanner
from spider import spider

URL = "http://127.0.0.1:5000"

pages = spider(URL)
print(pages)

for page in pages:
    scanner(URL, page)
