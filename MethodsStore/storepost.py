import requests

URL = "http://127.0.0.1:8090/store"

todo = {"name":"new Store","cnpj":"4939933004-654","email":"newstore@gmmail.com"}

response = requests.post(URL, json=todo)
print(response.status_code)

