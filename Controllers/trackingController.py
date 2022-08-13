import random
from Models import Tracking
import string
from flask import jsonify
base_cod = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
size = 10
def cod_generator(size = 35,chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars)for _ in range(size))
def store(id_request):
    tracking = Tracking(
        cod = cod_generator(size,base_cod),
        id_request = id_request,
        status_activate = 1
    )
    response = Tracking.insert(tracking)
    if response == 201:
        return jsonify({'msg':'Insert Successful', 'success':True}),200
    return jsonify({'msg':'not Json'}),415

def show(id_tracking):
    Response = Tracking.get_id(id_tracking)
    if Response == 405:
        return 405
    return Response
