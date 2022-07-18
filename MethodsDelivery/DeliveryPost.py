import requests

url = "http://127.0.0.1:8090/delivery/requests/1"

todo = {"shipping": 134.5}

response = requests.post(url, json = todo)

print(response.status_code)