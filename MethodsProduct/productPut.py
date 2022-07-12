import requests

URL = "http://10.112.4.118:8090/products/1"

todo = {"name":"Rolex new", "unitary_value":250.76,"weigth":0.15 }

response = requests.put(URL, json=todo)

print(response.status_code)