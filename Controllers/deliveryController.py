from Models import Delivery, Request
from flask import jsonify,request
from datetime import date, datetime, timedelta
from click import DateTime

def index(id_request):
    delivery = Delivery.get_all(id_request)
    if delivery == 405:
        return jsonify({'msg':'error'}),405
    return delivery,200

def show(id_delivery):
    delivery = Delivery.get_id(id_delivery)
    if delivery == 405:
        return jsonify({'msg':'error'}),405
    return delivery,200

def update(id_delivery,id_address):
    delivery = Delivery.get_id(id_delivery)
    if delivery is not None:
        delivery['id_address'] = id_address
        response = Delivery.update(delivery)
        if response == 200:
            return jsonify({'msg':'OK'}),200
        return jsonify({'msg':'error'}),405
    return jsonify({'msg':'not Json'}), 415

def store(id_request,id_address):

        response = Delivery.insert(id_request,id_address)
        if response == 201:
            return jsonify({'msg':'Insert Successful', 'success':True}),200
        return jsonify({'msg':'error'}),415

def delete(id):
    response = Delivery.delete(id)
    if response == 200:
        return jsonify({'msg':'success Delete'}),200
    return jsonify({'msg':'not found'}),405
    