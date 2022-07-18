import requests

URL = "http://127.0.0.1:8090/request/client/2"

response = requests.post(URL)

print(response.status_code)