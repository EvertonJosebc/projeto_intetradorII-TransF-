import re
import requests

URL = 'http://192.168.0.102:8090/client/store/1'

todo = {"name":"ALINE MORAIS","cpf":"095.655.455-99","phone":"88981045676"}

response = requests.post(URL, json=todo)

print(response.status_code)