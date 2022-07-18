import requests

URL = "http://127.0.0.1:8090/products/store/1"

todo = {"name":"Carrinho de Brinquedo","unitary_value":60.76,"weigth":0.950}

response = requests.post(URL, json = todo)

print(response.status_code)