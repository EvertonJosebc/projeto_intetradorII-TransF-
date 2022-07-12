import email
import requests
id=2
URL = "http://192.168.0.102:8090/store/{}".format(2)

todo = {"name":"bras","cnpj":"4939933004-001","email":"lojaodobras@gmail.com"}

response = requests.put(URL,json=todo)

print(response.status_code)