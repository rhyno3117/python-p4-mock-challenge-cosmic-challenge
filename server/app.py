#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>The Cosmic Code challenge</h1>'

#/////////////////////////////////////////////////////////////////////

@app.get('/scientists')
def get_scientists():
    scientists = Scientist.query.all()
    data = [scientist.to_dict(rules=('-missions',))for scientist in scientists]
    return make_response(jsonify(data),200)

@app.get('/scientists/<int:id>')
def get_scientists_by_id(id):
    scientists = Scientist.query.filter(Scientist.id == id).first()
    if not scientists:
        return make_response(jsonify({'error': 'Scientist not found'}),404)
    
    return make_response(jsonify(scientists.to_dict()),200)

@app.post('/scientists')
def post_scientists():
    data = request.get_json()
    try:
        new_scientist = Scientist(
            name = data['name'],
            field_of_study = data['field_of_study']
        )
        db.session.add(new_scientist)
        db.session.commit()
    except Exception:
        return make_response({"errors": ["validation errors"]}, 422)
    return make_response(new_scientist.to_dict(), 201)
    
@app.patch('/scientists/<id>')
def patch_scientists(id):
    sci = Scientist.query.filter_by(id=id).first()
    data = request.get_json()
    if not sci:
        return make_response({'error': 'Scientist not found'}, 404)
    try:
        for field in data:
            setattr(sci, field, data[field])
    except:
        return make_response({'error': ['Validation erros']}, 422)
    db.session.commit()
    return make_response(sci.to_dict(), 202)

@app.delete("/scientists/<int:id>")
def delete_scientists(id):
    sci = Scientist.query.filter_by(id=id).first()
    if not sci:
        return make_response({"error": "Scientist not found"}, 404)
    db.session.delete(sci)
    db.session.commit()

    return make_response({"message": "This is great"}, 226)










#/////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    app.run(port=5555, debug=True)
