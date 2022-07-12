import requests

URL = "http://192.168.0.102:8090/client/2"

todo = {"name":"Fabio Rocha","cpf":"9834883883","phone":"232399922"}

response = requests.put(URL,json=todo)

print(response.status_code)