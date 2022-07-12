import requests

URL = "http://192.168.0.102:8090/store/2"

response = requests.delete(URL)

print(response.status_code)