import requests

data = {"username": "Демо_тензор", "password": "Демо123"}
headers = {"X-SBISAccessToken": "313337-1337-asdq23-12ed122"}
r = requests.post("https://online.sbis.ru", data=data, headers=headers)
print(r.html)