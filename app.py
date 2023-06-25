import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'Secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class QuotesFlaskCurd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(1000))
    author = db.Column(db.String(100))

    def __init__(self, quote, author):
        self.quote = quote
        self.author = author


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    get_data = QuotesFlaskCurd.query.all()
    return jsonify({'message': f'{get_data}'})


@app.route('/random')
def random():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()
    if data:
        quote = data[0]['q']
        author = data[0]['a']
        return jsonify(f"{quote} - {author}")
    return jsonify("NULL")


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        quote = request.form['quote']
        author = request.form['author']

        my_data = QuotesFlaskCurd(quote, author)
        db.session.add(my_data)
        db.session.commit()
        return jsonify({'message': 'Data inserted successfully'})


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        quote_id = request.form['id']
        quote = request.form['quote']
        author = request.form['author']

        quote_data = QuotesFlaskCurd.query.get(quote_id)
        quote_data.quote = quote
        quote_data.author = author
        db.session.commit()

        return jsonify({'message': 'Data updated successfully'})


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    quote_data = QuotesFlaskCurd.query.get(id)
    db.session.delete(quote_data)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully'})

if __name__ == "__main__":
    app.run()
