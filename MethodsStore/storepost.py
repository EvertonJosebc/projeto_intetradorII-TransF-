import requests

URL = "http://192.168.0.102:8090/store"

todo = {"name":"Lojão do Bras","cnpj":"4939933004-001","email":"lojaodobras@gmmail.com"}



response = requests.post(URL, json=todo)
print(response.status_code)

