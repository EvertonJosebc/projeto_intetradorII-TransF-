import requests
url = "http://127.0.0.1:8090/calculate_shipping"

todo = {"destiny":"São Paulo/SP"}

response = requests.post(url, json = todo)
print(response.json())
print(response.status_code)