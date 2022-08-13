from os import stat
from flask import jsonify,request
import requests
from Models import Client

def index(id_store):
    client = Client.get_all(id_store)
    if client == 405:
            return jsonify({'msg':'error'}),405
    return client,200

def show(id_client):
    client = Client.get_id(id_client)
    if client == 405:
        return jsonify({'msg':'error'}),405
    return client,200

def update(id):
    Response = Client.update(id)
    if Response == 200:
        return {'msg':'OK'},200
    if Response == 415:
        return {'msg': "not Json"}, 415
    if Response == 405:
        return {'msg':'not found'},405



def store(id_store):
    if request.get_json:
        clientJson = request.get_json()
        client = Client(
            name = clientJson['name'],
            cpf = clientJson['cpf'],
            phone = clientJson['phone'],
            status_activate = 1,
            id_store = id_store

        )
        response = Client.insert(client)
        if response == 201:
            return jsonify({'msg':'Insert Successful', 'success':True}),200
        return jsonify({'msg':'error'}),415

def delete(id):
    response = Client.delete(id)
    if response == 200:
        return jsonify({'msg':'success Delete'}),200
    return jsonify({'msg':'not found'}),405
    
        
    