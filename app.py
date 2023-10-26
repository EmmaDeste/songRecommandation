from flask import Flask, render_template, request, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pickle as pk
import pandas as pd
from getsong import get_song

app = Flask(__name__)

# Set the secret key
app.secret_key = 'DaTaCaMP'

################################################################ Configuration de la connexion à la base de données #################################################################
# données fournies par Azure lors de la création du service web app sur Azure
app.config['MYSQL_HOST'] = 'localhost'  # /!\ commenter la ligne ci-dessous pour faire tourner en local
#app.config['MYSQL_HOST'] = 'groovegenius-server'
app.config['MYSQL_USER'] = 'loprdfhypz'
app.config['MYSQL_PASSWORD'] = '15N580424P852440$'
app.config['MYSQL_DB'] = 'groovegenius-database'

################################################################ Définition de l'URL de connexion à la base de données #################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}"

db = SQLAlchemy(app)

# Model for the songs table :
class Songs(db.Model):
    __tablename__ = 'songs'
    artist = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), primary_key=True, nullable=False)
    album = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)    # pour accepter les longs textes
    dim1 = db.Column(db.String(50), nullable=False)
    score1 = db.Column(db.Float, nullable=False)
    dim2 = db.Column(db.String(50), nullable=False)
    score2 = db.Column(db.Float, nullable=False)
    dim3 = db.Column(db.String(50), nullable=False)
    score3 = db.Column(db.Float, nullable=False)

# TODO: à supprimer
# thanks to https://pythonbasics.org/flask-sqlalchemy/
# Class to store the data
class SongsData:
    # Configuration de la BDD
    def __init__(self, artist, title, album, lyrics, dim1, score1, dim2, score2, dim3, score3):
        self.artist = artist
        self.title = title
        self.album = album
        self.lyrics = lyrics
        self.dim1 = dim1
        self.score1 = score1
        self.dim2 = dim2
        self.score2 = score2
        self.dim3 = dim3
        self.score3 = score3

################################################################ Vérification de la connexion à la base de données #################################################################
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))  # Utilisez text("SELECT 1")
        db.create_all()  # 1. Creation de la BDD
        print("La connexion à la base de données a été établie avec succès.")
    except Exception as e:
        print("Erreur lors de la connexion à la BDD:", str(e))


################################################################ Routage pour les pages #################################################################
@app.route('/')
def home():
    try:
        songs = Songs.query.all()
        return render_template('home.html', songs=songs)
    except Exception as e:
        print("Erreur dans le fetch de la BDD :", str(e))


@app.route('/init')  # TODO: besoin d'une méthode ?
def init():          # TODO: besoin d'une route ou déjà fait avec db.create_all() ?
    try:
        return "<p> INIT route </p>"
    except Exception as e:
        print("Erreur lors de l'initialisation de la BDD :", str(e))

@app.route('/fill', methods=['GET'])  # TODO: est-ce vraiment une méthode get ?
def fill():
    try:
        with open('DF_Song.pkl', 'rb') as file:
            data_songs = pk.load(file)
        fill_db(data_songs)

        return "<p> FILL route </p>"

    except Exception as e:
        print("Erreur lors du remplissage de la BDD :", str(e))

@app.route('/transform', methods=['GET'])  # TODO: est-ce vraiment une méthode get ?
def transform():    # Rempli la classe Songs data
    try:
        print(table_to_df())
        return "<p> TRANSFORM route </p>"
    except Exception as e:
        print("Erreur lors de la transformation en classe :", str(e))


@app.route('/result', methods=['POST'])
def result():
    try:
        print("enter result page")
        print("ask song1")
        song1 = request.form.get('song1')
        A1, T1 = song1.split(' - ')  # careful about - in titles, to avoid "too many values to unpack (expected 2)" error
        print("ask song2")
        song2 = request.form.get('song2')
        A2, T2 = song2.split(' - ')
        print("ask song3")
        song3 = request.form.get('song3')

        print("son1g", song1,"son2g", song2, "son3g", song3)

        songs = Songs.query.all()

        print("avant les if")
        if song3:
            print("song3 existe")
            A3, T3 = song3.split(' - ')
            # Verify that the songs are in the database :
            exist1 = Songs.query.filter_by(artist=A1, title=T1).first()
            exist2 = Songs.query.filter_by(artist=A2, title=T2).first()
            exist3 = Songs.query.filter_by(artist=A3, title=T3).first()
            if (exist1 is not None) and (exist2 is not None) and (exist3 is not None):
                #
                # code to analyse the preferencies
                #
                print("T3 exists")
                list_song = get_song(T1, T2, T3) #penser à changer une fois l'importation de df faite
                song_recomended1 = list_song[0]
                song_recomended2 = list_song[1]
                song_recomended3 = list_song[2]
                # song_recomended1 = 'Camille - Le thé du matin'
                return render_template('result.html', reco1=song_recomended1, reco2=song_recomended2,
                                       reco3=song_recomended3, songs=songs)
            else:
                flash('One of the songs that you choose is not into our database', 'danger')
                # Redirect to home page
                return redirect(url_for('home'))
        else:
            print("song3 n'existe pas")
            exist1 = Songs.query.filter_by(artist=A1, title=T1).first()
            exist2 = Songs.query.filter_by(artist=A2, title=T2).first()
            if (exist1 is not None) and (exist2 is not None):
                #
                # code to analyse the preferencies
                #
                print("T3 NO exists")
                list_song = get_song(T1, T2)
                song_recomended1 = list_song[0]
                song_recomended2 = list_song[1]
                song_recomended3 = list_song[2]
                # song_recomended1 = 'Camille - Juste pour deux chansons'
                return render_template('result.html', reco1=song_recomended1, reco2=song_recomended2,
                                       reco3=song_recomended3, songs=songs)
            else:
                flash('One of the songs that you choose is not into our database', 'danger')
                # Redirect to home page
                return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('An error occurred, please try again', 'danger')
        # Redirect to home page
        return redirect(url_for('home'))

@app.route('/test')
def test():
    return "<p> Bonjour, Emma, Noa, Camille ;-) </p>"

if __name__ == "__main__":
    app.run()

#####################################################################Fill the DB########################################################################""
#Creer d'abord la db avec toutes les col (vérifier que noms dans le fill_db = noms dcol dans db) + l'appeler songs normalement sinon modifier dans le insert et dans la classe le nom de la table
# verifier que les mêmes noms de col dans db
def fill_db(df):
    try:
        with db.session.begin():
            for i in df.index:
                db.session.execute(
                    text("INSERT INTO songs (artist, title, album, lyrics, dim1, score1, dim2, score2, dim3, score3) VALUES (:artist, :title, :album, :lyrics, :dim1, :score1, :dim2, :score2, :dim3, :score3)"),
                    {"artist": df["artist"][i],
                     "title": df["title"][i],
                     "album": df["album"][i],
                     "lyrics": df["lyrics"][i],
                     "dim1": df["dim1"][i],
                     "score1": df["score1"][i],
                     "dim2": df["dim2"][i],
                     "score2": df["score2"][i],
                     "dim3": df["dim3"][i],
                     "score3": df["score3"][i]
                    }
                )
    except Exception as e:
        print("Erreur dans le remplissage de la base de données:", str(e))

def table_to_df():
    songs_entries = Songs.query.all()  # <=> select *
    # attribue les données au paramètre (colonne) correspondant
    data = {
        'artist': [entry.artist for entry in songs_entries],
        'title': [entry.title for entry in songs_entries],
        'album': [entry.album for entry in songs_entries],
        'lyrics': [entry.lyrics for entry in songs_entries],
        'dim1': [entry.dim1 for entry in songs_entries],
        'score1': [entry.score1 for entry in songs_entries],
        'dim2': [entry.dim2 for entry in songs_entries],
        'score2': [entry.score2 for entry in songs_entries],
        'dim3': [entry.dim3 for entry in songs_entries],
        'score3': [entry.score3 for entry in songs_entries]}

    df = pd.DataFrame(data)
    return df

def emoji_identifier(df):
    if df['dim1'] == 'Joy':
        return True
    if df['dim2'] == 'Anger':
        return True
    if df['dim3'] == 'Sadness':
        return True
    if df['dim4'] == 'Love':
        return True
    if df['dim5'] == 'Nostalgia':
        return True
    if df['dim6'] == 'Fear':
        return True
    if df['dim7'] == 'Hope':
        return True
