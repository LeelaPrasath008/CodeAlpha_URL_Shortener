from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy

import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(200), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Hello Backend Intern!"

@app.route('/api/test')
def test_api():
    return jsonify({
        "message": "API Working Successfully",
        "status": "success"
    })

@app.route('/leela')
def leela():
    return jsonify({
        "zebra": 1,
        "apple": 2,
        "monkey": 3
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    url = data["url"]
    characters = string.ascii_letters + string.digits
    short_code = ''.join(
        random.choice(characters)
        for _ in range(6)
    )
    url_database[short_code] = url
    return jsonify({
        "original_url": url,
        "short_code": short_code
    })

@app.route('/generate')
def generate():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(
        random.choice(characters)
        for _ in range(6)
    )
    return jsonify({
        "short_code": short_code
    })

@app.route('/<short_code>')
def redirect_url(short_code):

    if short_code in url_database:

        original_url = url_database[short_code]

        return redirect(original_url)

    return jsonify({
        "error": "Short URL not found"
    }), 404

@app.route('/all')
def all_urls():
    return jsonify(url_database)

if __name__ == '__main__':
    app.run(debug=True)