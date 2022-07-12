from urllib import response
import requests

URL = "http://192.168.0.102:8090/address/1"

todo = {"locality":"JOSE FERREIA","local":"RUA","discrict":"CENTRO","cep":"59980000","number":"SN"}
response = requests.put(URL, json= todo)

print(response.status_code)