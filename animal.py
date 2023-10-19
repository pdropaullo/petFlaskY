from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senac2021@localhost:3306/petflask'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Animal(db.Model):
   __tablename__ = "animais"
   id = db.Column(db.Integer, primary_key=True)
   nome = db.Column(db.String(100))
   especie = db.Column(db.String(100))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, nome, especie):
       self.nome = nome
       self.especie = especie

   def __repr__(self):
       return f"{self.id}"

class AnimalSchema(ma.Schema):
   class Meta(ma.Schema.Meta):
       model = Animal
       sqla_session = db.session
   id = fields.Number(dump_only=True)
   nome = fields.String(required=True)
   especie = fields.String(required=True)

@app.route('/api/v1/animal', methods=['POST'])
def create_animal():
   data = request.get_json()
   animal_schema = AnimalSchema()
   animal = animal_schema.load(data)
   result = animal_schema.dump(animal.create())
   return make_response(jsonify({"animal": result}), 200)

@app.route('/api/v1/animal', methods=['GET'])
def index():
   get_animais = Animal.query.all()
   animal_schema = AnimalSchema(many=True)
   animais = animal_schema.dump(get_animais)
   return make_response(jsonify({"animais": animais}))

@app.route('/api/v1/animal/<id>', methods=['GET'])
def get_animal_by_id(id):
   get_animal = Animal.query.get(id)
   animal_schema = AnimalSchema()
   animal = animal_schema.dump(get_animal)
   return make_response(jsonify({"animal": animal}))

@app.route('/api/v1/animal/<id>', methods=['PUT'])
def update_animal_by_id(id):
   data = request.get_json()
   get_animal = Animal.query.get(id)
   if data.get('nome'):
       get_animal.nome = data['nome']
   if data.get('especie'):
       get_animal.especie = data['especie']
   db.session.add(get_animal)
   db.session.commit()
   animal_schema = AnimalSchema(only=['id', 'nome', 'especie'])
   animal = animal_schema.dump(get_animal)

   return make_response(jsonify({"animal": animal}))

@app.route('/api/v1/animal/<id>', methods=['DELETE'])
def delete_animal_by_id(id):
   get_animal = Animal.query.get(id)
   db.session.delete(get_animal)
   db.session.commit()
   return make_response("", 204)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

