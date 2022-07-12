import requests

URL = "http://192.168.0.102:8090/client/3"

response = requests.delete(URL)

print(response.status_code)