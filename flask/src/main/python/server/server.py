from flask import Flask, request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)



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
def get():
    all_users = Task.query.all()
    result = tasks_schema.dump(all_users)
    #print(jsonify(result.data))
    return jsonify(result.data)

@app.route('/',methods=['POST'])
def post():
    if "name" not in request.json:
        print("nix da")
    name = request.json["name"]
    description = request.json["description"]

    t = Task(name,description)
    db.session.add(t)
    db.session.commit()
    return "Sucessfully added a new task"

if __name__=="__main__":
    db.drop_all()
    db.create_all()
    try:
        t = Task('testTask','db auffuellen')
        print("created task")
        print(t)
        db.session.add(t)
        db.session.commit()
    except:
        pass
    finally:
        tasks = Task.query.all()
        tasks_schema.dump(tasks)

        app.run(debug=True)