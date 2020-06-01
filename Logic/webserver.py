from flask import Flask
from flask import jsonify
from Logic.control import Control

control = Control()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify(control.get_events())

if __name__ == '__main__':
    app.run(debug=True)