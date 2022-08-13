from Models import Store

from flask import request, jsonify


def index():
    store = Store.get_all()
    if store == 405:
        return jsonify({'msg':'error'}),405
    return store,200

def show(id_store):
    store = Store.get_id(id_store)
    if store == 405:
        return jsonify({'msg':'error'}),405
    return store,200

def update(id):
    Response = Store.update(id)
    if Response == 200:
        return {'msg':'OK'},200
    if Response == 415:
        return {'msg': "not Json"}, 415
    if Response == 405:
        return {'msg':'not found'},405


def store():
    if request.get_json:
        storeJson = request.get_json()
        store = Store(name = storeJson['name'],cnpj = storeJson['cnpj'],email = storeJson['email'], status_activate = 1 )

        Response = Store.insert(store)
        if Response == 201:
            return jsonify({'msg':'Insert Successful', 'success':True}),201
        return {'msg':'error'},415


def delete(id):
    response = Store.delete(id)
    if response == 200:
        return jsonify({'msg':'success Delete'}),200
    return jsonify({'msg':'not found'}),405
    