import cProfile
from config import db
from flask import jsonify, request

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(14))
    phone = db.Column(db.String(50))
    id_store = db.Column(db.Integer,db.ForeignKey("store.id"))
    status_activate = db.Column(db.Integer)
    def json_return(self):
        return {
            "id": self.id,
            "name": self.name,
            "cpf": self.cpf,
            "phone": self.phone,
            "id_store": self.id_store,
            "status_activate": self.status_activate
        }

#insert client
    def insert(client):
        db.session.add(client)
        db.session.commit()
        return 201

#all client
    def get_all(id_store):
        client = Client.query.filter_by(id_store=id_store).all()
        if client is not None:
            return jsonify([c.json_return() for c in client])
        return 405
#id client get
    def get_id(id):
        client = Client.query.get(id)
        if client is not None:
            return jsonify(client.json_return())
        return 405
#update client
    def update(id):
        client = Client.query.get(id)
        if client is not None:
            if request.is_json:
                clientJson = request.get_json()
                if ("name" in clientJson):
                    client.name = clientJson['name']
                if ("cpf" in clientJson):
                    client.cpf = clientJson['cpf']
                if ("phone" in clientJson):
                    client.phone = clientJson['phone']
                db.session.add(client)
                db.session.commit()
                return 200
            return 415
        return 405
                

        
#delete client

    def delete(id):
        client = Client.query.get(id)
        if client is not None:
            client.status_activate = 0
            db.session.add(client)
            db.session.commit()
            return 200
        return 405