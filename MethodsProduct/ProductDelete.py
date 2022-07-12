import requests

URL = 'http://10.112.4.118:8090/products/1'

response = requests.delete(URL)

print(response.status_code)