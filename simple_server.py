from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Simple Flask Server!"})


@app.route('/hello')
def hello():
    return jsonify({"message": "Hello, World!"})


@app.route('/about')
def about():
    return jsonify({
        "name": "Simple Flask Server",
        "version": "1.0",
        "description": "A simple Flask server with basic routes"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
