from flask import Flask, request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db2 = SQLAlchemy(app)
ma2 = Marshmallow(app)

auth = HTTPBasicAuth()


class User(db2.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

@auth.get_password
def get_pw(username):
    user = User.query.filter_by(username=username).first()
    if user.username == username:
        return user.password
    return None


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class TaskSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "description")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/',methods=['GET'])
@auth.login_required
def get_all():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result.data)

@app.route('/<id>', methods=['GET'])
@auth.login_required
def get(id):
    task = Task.query.filter_by(id=id).first()
    result = task_schema.dump(task)
    return jsonify(result.data)

@app.route('/',methods=['POST'])
@auth.login_required
def post():
    if "name" not in request.json:
        raise ValueError("Name is a must have")
    if "description" not in request.json:
        raise ValueError("Task description is a must have")

    name = request.json["name"]
    description = request.json["description"]

    t = Task(name,description)
    db.session.add(t)
    db.session.commit()
    result = task_schema.dump(t)
    return jsonify(result.data)

@app.route('/<id>', methods=['PUT'])
@auth.login_required
def put(id):
    task = Task.query.filter_by(id=id).first()
    name = task.name
    description = task.description
    print(request.json)
    if "name" in request.json:
        name = request.json["name"]
    if "description" in request.json:
        description = request.json["description"]

    task.name = name
    task.description = description
    db.session.commit()
    result = task_schema.dump(task)
    return jsonify(result.data)

@app.route('/<id>', methods=['DELETE'])
@auth.login_required
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    result = task_schema.dump(task)
    return jsonify(result.data)

def initTaskDb():
    db.drop_all()
    db.create_all()
    try:
        t = Task('testTask', 'db auffuellen')
        db.session.add(t)
        db.session.commit()
    except:
        pass
    finally:
        tasks = Task.query.all()
        tasks_schema.dump(tasks)

def initUserDb():
    db2.drop_all()
    db2.create_all()
    try:
        u = User('admin', '1234')
        db2.session.add(u)
        db2.session.commit()
    except:
        pass
    finally:
        return

if __name__=="__main__":
    initTaskDb()
    initUserDb()

    app.run(debug=True)