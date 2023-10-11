from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

#/////////////////////////////////////////////////////////////////////

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    missions = db.relationship("Mission", backref="planet")

#/////////////////////////////////////////////////////////////////////

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    missions = db.relationship("Mission", backref="scientist", cascade= "all, delete")

#/////////////////////////////////////////////////////////////////////

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists_table.id"),nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets_table.id"),nullable=False)

    serialize_rules=('-planet.missions','-scientist')



