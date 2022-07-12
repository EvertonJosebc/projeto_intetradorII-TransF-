import requests

URL = "http://192.168.0.102:8090/address/1"

response = requests.delete(URL)

print(response.status_code)

