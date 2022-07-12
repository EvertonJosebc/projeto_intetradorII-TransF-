import requests

URL = "http://10.112.4.118:8090/products/store/1"

todo = {"name":"Armario de parede de aço","unitary_value":1200.56,"weigth":300}

response = requests.post(URL, json = todo)

print(response.status_code)