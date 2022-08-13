from hashlib import new
import json
from Models import Address
from flask import jsonify,request
import requests

def index(id_client):
    address = Address.get_all(id_client)
    if address == 405:
        return  jsonify({'msg':'error'}),405
    return address,200
    
def show(id_address):
    address = Address.get_id(id_address)
    if address == 405:
        return  jsonify({'msg':'error'}),405
    return address,200

def update(id):
    Response = Address.update(id)
    if Response == 200:
        return {'msg':'OK'},200
    if Response == 415:
        return {'msg': "not Json"}, 415
    if Response == 405:
        return {'msg':'not found'},405
    


def store(id_client):
    if request.get_json:
        addressJson = request.get_json()
        URL = 'https://ws.apicep.com/cep/{}.json'
        cep = addressJson['cep']
        response = requests.get(URL.format(cep))
        if response.status_code == 200:
            responseJson = response.json()
            address = Address(locality = addressJson['locality'],local = addressJson['local'], district = addressJson['district'],number = addressJson['number'],id_client = id_client,cep = addressJson['cep'],city = responseJson['city'],state = responseJson['state'],status_activate = 1)
            Response = Address.insert(address)
        else:
            address = Address(locality = addressJson['locality'],local = addressJson['local'], district = addressJson['district'],number = addressJson['number'],id_client = id_client,cep = addressJson['cep'],city = 'Not Found',state = 'Not Found',status_activate = 1)
            Response = Address.insert(address)
        
        if Response == 201:
            return jsonify({'msg':'Insert Successful', 'success':True}),201
        return {'msg':'error'},415

def delete(id):
    response = Address.delete(id)
    if response == 200:
        return jsonify({'msg':'success Delete'}),200
    return jsonify({'msg':'not found'}),405
    

