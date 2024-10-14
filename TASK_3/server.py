from flask import Flask, jsonify, request, redirect
from flask_swagger_ui import get_swaggerui_blueprint
import random
import webbrowser
import threading

app = Flask(__name__)

# Swagger UI Configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Flask API Server"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return redirect('/swagger', code=302)  


@app.route('/inverse', methods=['POST'])
def inverse():
    data = request.get_json()
    inverted_data = {v: k for k, v in data.items()}
    return jsonify(inverted_data), 200

@app.route('/unstable', methods=['GET'])
def unstable():
    if random.random() < 0.5:
        return jsonify(message="HAPPY"), 200
    else:
        return jsonify(message="UNHAPPY"), 400

def open_swagger():
    webbrowser.open_new('http://127.0.0.1:5000/swagger')

if __name__ == '__main__':
    threading.Timer(1, open_swagger).start()
    app.run(debug=True)
