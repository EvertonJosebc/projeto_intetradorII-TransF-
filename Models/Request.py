from config import db
from flask import jsonify
from .Client import Client
class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
    id_store = db.Column(db.Integer, db.ForeignKey('store.id'))
    status_activate = db.Column(db.Integer)

    def return_json(self):
        return {
            'id': self.id,
            'id_client': self.id_client,
            'id_store': self.id_store,
            'status_activate': self.status_activate
            }
#insert Request
    def insert(id_client):
        client = Client.query.get(id_client)
        request = Request(
            id_client = id_client,
            id_store = client.id_store,
            status_activate = 1
        )
        db.session.add(request)
        db.session.commit()
        return 201
#all Request
    def get_all(id_client):
        request = Request.query.filter_by(id_client=id_client).all()
        if request is not None:
            return jsonify([r.return_json() for r in request])
        return 405
#id Request get
    def get_id(id):
        request = Request.query.get(id)
        if request is not None:
            return jsonify(request.return_json())
        return 405
#update Request
    def update(id):
        request = Request.query.get(id)
        if request is not None:
            db.session.add(Request)
            db.session.commit()
            return 
        return 405
       
#delete Request

    def delete(id):
        request = Request.query.get(id);
        if request is not None:
            request.status_activate = 0
            db.session.add(request)
            db.session.commit()
            return 200
        return 405