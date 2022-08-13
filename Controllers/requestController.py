from multiprocessing.connection import Client
from Models import Request, Client
from flask import request,jsonify
import json

def index(id_client):
    request = Request.get_all(id_client)
    if request == 405:
        return jsonify({'msg':'error'}),405
    return request,200

def show(id_request):
    request = Request.get_id(id_request)
    if request == 405:
        return jsonify({'msg':'error'}),405
    return request,200

def update(id):
    Response = Request.update(id)
    if Response == 200:
        return {'msg':'OK'},200
    if Response == 415:
        return {'msg': "not Json"}, 415
    if Response == 405:
        return {'msg':'not found'},405


def store(id_client):
        response = Request.insert(id_client)
        if response == 201:
            return jsonify({'msg':'Insert Successful', 'success':True}),201
        return jsonify({'msg':'error'}),415
        

def delete(id):
    response = Request.delete(id)
    if response == 200:
        return jsonify({'msg':'success Delete'}),200
    return jsonify({'msg':'not found'}),405