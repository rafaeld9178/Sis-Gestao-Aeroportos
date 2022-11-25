from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Airport(db.Model):
    id_aeroporto = db.Column(db.Integer, primary_key=True)
    nome_aeroporto = db.Column(db.String(100))
    codigo_iata = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    codigo_pais_iso = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)


    def __init__(self, nome_aeroporto, codigo_iata, cidade, codigo_pais_iso, latitude, longitude, altitude):
        self.nome_aeroporto = nome_aeroporto
        self.codigo_iata = codigo_iata
        self.cidade = cidade
        self.codigo_pais_iso = codigo_pais_iso
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

class AirportSchema(ma.Schema):
    class Meta:
        fields = ('id_aeroporto', 'nome_aeroporto', 'codigo_iata', 'cidade', 'codigo_pais_iso', 'latitude', 'longitude', 'altitude')

airport_schema = AirportSchema()
airport_all_schema = AirportSchema(many=True)

@app.route('/aeroporto', methods=['POST'])
def add_airport():
    nome_aeroporto = request.json['nome_aeroporto']
    codigo_iata = request.json['codigo_iata']
    cidade = request.json['cidade']
    codigo_pais_iso = request.json['codigo_pais_iso']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    altitude = request.json['altitude']

    novo_aeroporto = Airport(nome_aeroporto, codigo_iata, cidade, codigo_pais_iso, latitude, longitude, altitude)
    db.session.add(novo_aeroporto)
    db.session.commit()

    return airport_schema.jsonify(novo_aeroporto)

@app.route('/aeroporto', methods=['GET'])
def get_all_airports():
    all_airports = Airport.query.all()
    result = airport_all_schema.dump(all_airports)
    return jsonify(result)

@app.route('/aeroporto/<id_aeroporto>', methods=['GET'])
def get_airport(id_aeroporto):
    airport = Airport.query.get(id_aeroporto)
    return airport_schema.jsonify(airport)

@app.route('/aeroporto/<id_aeroporto>', methods=['PUT'])
def update_airport(id_aeroporto):
    airport = Airport.query.get(id_aeroporto)
    nome_aeroporto = request.json['nome_aeroporto']
    codigo_iata = request.json['codigo_iata']
    cidade = request.json['cidade']
    codigo_pais_iso = request.json['codigo_pais_iso']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    altitude = request.json['altitude']

    airport.nome_aeroporto = nome_aeroporto
    airport.codigo_iata = codigo_iata
    airport.cidade = cidade
    airport.codigo_pais_iso = codigo_pais_iso
    airport.latitude = latitude
    airport.longitude = longitude
    airport.altitude = altitude

    db.session.commit()

    return airport_schema.jsonify(airport)

@app.route('/aeroporto/<id_aeroporto>', methods=['DELETE'])
def delete_airport(id_aeroporto):
    airport = Airport.query.get(id_aeroporto)
    db.session.delete(airport)
    db.session.commit()
    return airport_schema.jsonify(airport)


if __name__ == '__main__':
    app.run(debug=True)