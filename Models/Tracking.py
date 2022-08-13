from config import db
from flask import jsonify

class Tracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cod = db.Column(db.String(12))
    id_request = db.Column(db.Integer, db.ForeignKey('request.id'))
    status_activate = db.Column(db.Integer)

    def return_json(self):
        return {
            'id': self.id,
            'cod': self.cod,
            'status_activate': self.status_activate,
            'id_request': self.id_request
        }

#insert Tracking
    def insert(Tracking):
        db.session.add(Tracking)
        db.session.commit()
        return 201
#all Tracking
    def get_all(id_Tracking):
        tracking = Tracking.query.filter_by(id_Tracking=id_Tracking).all()
        if tracking is not None:
            return jsonify(tracking.return_json())
        return 405
#id Tracking get
    def get_id(id):
        tracking = Tracking.query.get(id)
        if tracking is not None:
            return jsonify(tracking.return_json())
        return 405
#update Tracking
    def update(Tracking):
        if Tracking is not None:
            db.session.add(Tracking)
            db.session.commit()
            return 200
        return 405
#delete Tracking

    def delete(Tracking,self):
        return self.update(Tracking)