from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn

db = SQLAlchemy(app)


class tgeisler_pokemonapp(db.Model):
    pokemonID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))


class PokemonForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    type = StringField('Type:', validators=[DataRequired()])


@app.route('/')
def index():
    all_pokemon = tgeisler_pokemonapp.query.all()
    return render_template('index.html', friends = all_pokemon, pageTitle='Flask Server Home Page')


@app.route('/add_pokemon', methods=['GET', 'POST'])
def add_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        pokemon = tgeisler_pokemonapp(name=form.name.data, type=form.type.data)
        db.session.add(pokemon)
        db.session.commit()

        return redirect('/')
    
    return render_template('add_pokemon.html', form=form, pageTitle='Add a New Pokemon')


# @app.route('/pokemon/<int:pokemonID>', methods=['GET','POST'])
# def pokemon(pokemonID):
#     pokemon = tgeisler_pokemonapp.query.get_or_404(pokemonID)
#     return render_template('pokemon.html', form=pokemon, pageTitle='Pokemon Details')


# @app.route('/pokemon/<int:pokemonID>/update', methods=['GET','POST'])
# def update_pokemon(pokemonID):
#     pokemon = tgeisler_pokemonapp.query.get_or_404(pokemonID)
#     form = PokemonForm()
#     if form.validate_on_submit():
#         pokemon.name = form.name.data
#         pokemon.type = pokemon.type.data
#         db.session.commit()
#         return redirect(url_for('pokemon', pokemonID=pokemon.pokemonID))
#     form.name.data = pokemon.name
#     form.type.data = pokemon.type
#     return render_template('add_pokemon.html', form=form, pageTitle='Update Post')


# @app.route('/pokemon/<int:pokemonID>/delete', methods=['POST'])
# def delete_pokemon(friend_id):
#     if request.method == 'POST':
#         pokemon = tgeisler_pokemonapp.query.get_or_404(pokemonID)
#         db.session.delete(pokemon)
#         db.session.commit()
#         return redirect("/")
#     else:
#         return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
