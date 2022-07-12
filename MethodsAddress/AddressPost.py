import requests

URL = "http://192.168.0.102:8090/address/client/1"

todo = {"locality":"VEREADOR EDMILSON RODRIGUES DA SILVA","local":"RUA","discrict":"BAIRRO DUQUE DE CAXIAS","cep":"59980000","number":"41"}

response = requests.post(URL, json = todo)

print(response.status_code)