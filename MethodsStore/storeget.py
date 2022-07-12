import requests

URL = "http://192.168.0.102:8090/store"

response = requests.get(URL)

print(response.json())
print(response.status_code)