from urllib import response
import requests

URL = "http://127.0.0.1:8090/request/products/3/4"

todo = {"quantity": 2}

response = requests.post(URL,json=todo)

print(response.status_code)