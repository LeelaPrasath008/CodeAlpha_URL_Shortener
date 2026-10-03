from flask import Flask, jsonify, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string
from urllib.parse import urlparse



def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Model
class Url(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    short_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    original_url = db.Column(
        db.String(500),
        nullable=False
    )

    clicks = db.Column(
        db.Integer,
        default=0
    )


# Home Route
@app.route('/')
def home():
    return render_template('index.html')


# Create Short URL
@app.route('/api/shorten', methods=['POST'])
def shorten_url():

    data = request.get_json()

    url = data["url"]

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not is_valid_url(url):

        return jsonify({
            "error": "Invalid URL"
        }), 400


    while True:

        short_code = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=6
            )
        )

        existing_url = Url.query.filter_by(
            short_code=short_code
        ).first()

        if not existing_url:
            break

    new_url = Url(
        short_code=short_code,
        original_url=url
    )

    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "original_url": url,
        "short_code": short_code
    })


# View All URLs
@app.route('/db-all')
def db_all():

    urls = Url.query.all()
    result = []
    for url in urls:
        result.append({
            "id": url.id,
            "short_code": url.short_code,
            "original_url": url.original_url,
            "clicks": url.clicks
        })

    return jsonify(result)


# Redirect Route
@app.route('/<short_code>')
def redirect_url(short_code):

    url = Url.query.filter_by(
        short_code=short_code
    ).first()

    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)

    return jsonify({
        "error": "Short URL not found"
    }), 404


# Create Database Tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)