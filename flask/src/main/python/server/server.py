from flask import Flask

app = Flask(__name__)

tasks = {}

@app.route('/',methods=['GET'])
def get():
    return tasks

if __name__=="__main__":
    app.run(debug=True)