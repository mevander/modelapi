from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost/modelapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Init db
db = SQLAlchemy(app)
db.create_all()

#Init ma
ma = Marshmallow(app)

#Models
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)

    def __init__(self,username):
        self.username = username


#Schemas
class userSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username')


# Init schema
user_schema = userSchema()
users_schema = userSchema(many=True)


#EndPoints
@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


# Create a user
@app.route('/user', methods=['POST'])
def add_user():
  uname = request.form['username']

  new_user = user(uname)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)


# Get all users
@app.route('/user', methods=['GET'])
def get_users():
  all_users = user.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)


# Get single users
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
  usr = user.query.get(id)
  return user_schema.jsonify(usr)


# Update a user
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
  usr = user.query.get(id)
  username = request.json['username']
  usr.username = username
  db.session.commit()

  return user_schema.jsonify(usr)


# Delete user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  user = user.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)


#Run Server
if __name__=='__main__':
    app.run(debug=True)