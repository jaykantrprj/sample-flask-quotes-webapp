import os
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import psycopg2
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import requests



app = Flask(__name__)
app.secret_key = 'Secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:changeme@localhost:5432/quotes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class employee_flask_curd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

with app.app_context():
    db.create_all()
# db.create_all()

@app.route('/')
def index():
    get_data = employee_flask_curd.query.all()
    # return render_template('index.html', employees=get_data)
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
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = employee_flask_curd(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        # flash('Data inserted successfully.')
        # return redirect(url_for('index'))
        return jsonify({'message': 'Data inserted successfully'})

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        get_data = employee_flask_curd.query.get(request.form.get('id'))
        get_data.name = request.form['name']
        get_data.email = request.form['email']
        get_data.phone = request.form['phone']
        db.session.commit()
        flash('Data updated successfully.')
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    get_data = employee_flask_curd.query.get(id)
    db.session.delete(get_data)
    db.session.commit()
    flash('Data Delete successfully.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)