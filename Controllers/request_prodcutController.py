from Models import Request_product
from flask import request,jsonify

def store(id_request, id_product):
    if request.get_json:
        request_product_tJson = request.get_json()
        request_product = Request_product(
            quantity = request_product_tJson['quantity'],
            id_request = id_request,
            id_product = id_product
        )
        
        response = Request_product.insert(request_product)
        if response == 201:
            return jsonify({'msg':'ok'}),201
        return jsonify({'msg':'error'}),405
    return jsonify({'msg':'error not Json'}),415