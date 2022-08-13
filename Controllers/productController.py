from Models import Product
from flask import request, jsonify

def index(id_store):
    product = Product.get_all(id_store)
    if product == 405:
        return jsonify({'msg':'error'}),405
    return product,200

def show(id_product):
    product = Product.get_id(id_product)
    if product == 405:
        return jsonify({'msg':'error'}),405
    return product,200



def update(id):
    Response = Product.update(id)
    if Response == 200:
        return {'msg':'OK'},200
    if Response == 415:
        return {'msg': "not Json"}, 415
    if Response == 405:
        return {'msg':'not found'},405




def store(id_store):
    if request.get_json:
        productJson = request.get_json()
        product =Product(
            name = productJson['name'],
            unitary_value = productJson['unitary_value'],
            weigth = productJson['weigth'],
            id_store = id_store,
            status_activate = 1
        )
        response = Product.insert(product)
        if response == 201:
            return jsonify({'msg':'Insert Successful', 'success':True}),200
    return jsonify({'msg':'not Json'}),415

def delete(id):
    response = Product.delete(id)
    if response == 200:
        return jsonify({'msg':'success Delete'}),200
    return jsonify({'msg':'not found'}),405