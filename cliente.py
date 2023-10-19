from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senac2021@localhost:3306/petflask'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Cliente(db.Model):
   __tablename__ = "clientes"
   id = db.Column(db.Integer, primary_key=True)
   nome = db.Column(db.String(100))
   contato = db.Column(db.String(100))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, nome, contato):
       self.nome = nome
       self.contato = contato

   def __repr__(self):
       return f"{self.id}"

class ClienteSchema(ma.Schema):
   class Meta(ma.Schema.Meta):
       model = Cliente
       sqla_session = db.session
   id = fields.Number(dump_only=True)
   nome = fields.String(required=True)
   contato = fields.String(required=True)

@app.route('/api/v1/cliente', methods=['POST'])
def create_cliente():
   data = request.get_json()
   cliente_schema = ClienteSchema()
   cliente = cliente_schema.load(data)
   result = cliente_schema.dump(cliente.create())
   return make_response(jsonify({"cliente": result}), 200)

@app.route('/api/v1/cliente', methods=['GET'])
def index():
   get_clientes = Cliente.query.all()
   cliente_schema = ClienteSchema(many=True)
   clientes = cliente_schema.dump(get_clientes)
   return make_response(jsonify({"clientes": clientes}))

@app.route('/api/v1/cliente/<id>', methods=['GET'])
def get_cliente_by_id(id):
   get_cliente = Cliente.query.get(id)
   cliente_schema = ClienteSchema()
   cliente = cliente_schema.dump(get_cliente)
   return make_response(jsonify({"cliente": cliente}))

@app.route('/api/v1/cliente/<id>', methods=['PUT'])
def update_cliente_by_id(id):
   data = request.get_json()
   get_cliente = Cliente.query.get(id)
   if data.get('nome'):
       get_cliente.nome = data['nome']
   if data.get('contato'):
       get_cliente.contato = data['contato']
   db.session.add(get_cliente)
   db.session.commit()
   cliente_schema = ClienteSchema(only=['id', 'nome', 'contato'])
   cliente = cliente_schema.dump(get_cliente)

   return make_response(jsonify({"cliente": cliente}))

@app.route('/api/v1/cliente/<id>', methods=['DELETE'])
def delete_cliente_by_id(id):
   get_cliente = Cliente.query.get(id)
   db.session.delete(get_cliente)
   db.session.commit()
   return make_response("", 204)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

