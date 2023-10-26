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
#app.config['MYSQL_HOST'] = 'localhost'  # /!\ commenter la ligne ci-dessous pour faire tourner en local
app.config['MYSQL_HOST'] = 'groovegenius-server'
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
            exist1 = Songs.query.filter_by(artist=A1, title=T1)
            exist2 = Songs.query.filter_by(artist=A2, title=T2)
            exist3 = Songs.query.filter_by(artist=A3, title=T3)
            if (exist1 is not None) and (exist2 is not None) and (exist3 is not None):
                print("T3 exists")
                list_song = get_song(T1, T2, T3)
                song_recomended1 = list_song[0]
                song_recomended2 = list_song[1]
                song_recomended3 = list_song[2]

                titres_donnes = [T1, T2,T3]
                songs_info = db.session.query(Songs.title, Songs.dim1, Songs.score1, Songs.dim2, Songs.score2,
                                              Songs.dim3, Songs.score3).filter(
                    Songs.title.in_(titres_donnes)).all()
                df = pd.DataFrame(songs_info, columns=['title', 'dim1', 'score1', 'dim2', 'score2', 'dim3', 'score3'])
                print(df.head())
                print(emoji_identifier(get_main_sentiment(df)))
                emoji = emoji_identifier(get_main_sentiment(df))

                return render_template('result.html', reco1=song_recomended1, reco2=song_recomended2,
                                       reco3=song_recomended3, songs=songs, emoji=emoji)

            else:
                flash('One of the songs that you choose is not into our database', 'danger')
                # Redirect to home page
                return redirect(url_for('home'))
        else:
            print("song3 n'existe pas")
            exist1 = Songs.query.filter_by(artist=A1, title=T1)
            print(exist1)
            exist2 = Songs.query.filter_by(artist=A2, title=T2)
            print(exist2)
            print(A2)
            print(T2)
            if (exist1 is not None) and (exist2 is not None):
                print("T3 NO exists")
                list_song = get_song(T1, T2)
                song_recomended1 = list_song[0]
                song_recomended2 = list_song[1]
                song_recomended3 = list_song[2]

                titres_donnes = [T1, T2]
                songs_info = db.session.query(Songs.title, Songs.dim1, Songs.score1, Songs.dim2, Songs.score2, Songs.dim3, Songs.score3).filter(
                    Songs.title.in_(titres_donnes)).all()
                df = pd.DataFrame(songs_info, columns=['title', 'dim1', 'score1', 'dim2', 'score2', 'dim3', 'score3'])
                print(df.head())
                print(emoji_identifier(get_main_sentiment(df)))
                emoji = emoji_identifier(get_main_sentiment(df))

                return render_template('result.html', reco1=song_recomended1, reco2=song_recomended2,
                                       reco3=song_recomended3, songs=songs, emoji=emoji)
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

def get_main_sentiment(df):
    # Récupérer les noms des colonnes de sentiment et de score
    sentiment_columns = [col for col in df.columns if col.startswith('dim')]
    score_columns = [col for col in df.columns if col.startswith('score')]

    # Créer un dictionnaire pour stocker les totaux des scores par sentiment
    sentiment_totals = {}

    # Parcourir les colonnes de sentiment et de score
    for sentiment_col, score_col in zip(sentiment_columns, score_columns):
        sentiment = df[sentiment_col]
        score = df[score_col]

        for s, sc in zip(sentiment, score):
            if s in sentiment_totals:
                sentiment_totals[s] += abs(sc)
            else:
                sentiment_totals[s] = sc

    # Trouver le sentiment majoritaire en fonction des totaux des scores
    main_sentiment = max(sentiment_totals, key=sentiment_totals.get)
    print(main_sentiment)

    return main_sentiment

def emoji_identifier(sentiment):
    if sentiment == 'Joy':
        return "full of happiness 😄"
    if sentiment == 'Anger':
        return "in an angry mood... 😡"
    if sentiment == 'Sadness':
        return "sad presently... 🥺"
    if sentiment == 'Love':
        return "hyped up about love 🥰"
    if sentiment == 'Nostalgia':
        return "really nostalgic at the moment 😔"
    if sentiment == 'Fear':
        return "afraid of something currently 😨"
    if sentiment == 'Hope':
        return "hopeful for the future, sounds great 🤞"
    else:
        return "Come as you are!"
