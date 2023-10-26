from flask import Flask
from flask import Flask, render_template, request, jsonify, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

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
    lyrics = db.Column(db.String(255), nullable=False)
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
        print("La connexion à la base de données a été établie avec succès.")
    except Exception as e:
        print("Erreur lors de la connexion à la base de données:", str(e))


################################################################ Routage pour les pages #################################################################
@app.route('/')
def home():
    try:
        songs = Songs.query.all()
        return render_template('home.html', songs = songs)
    except Exception as e:
        print("Erreur dans le fetch de la base de données :", str(e))


@app.route('/init', methods = ['POST']) # TODO: besoin d'une méthode ?
def init():
    try:
        return "<p> INIT route </p>"
    except Exception as e:
        print("Erreur lors de l'initialisation de la base de données :", str(e))

@app.route('/fill', methods = ['GET']) # TODO: est-ce vraiment une méthode get ?
def fill():
    try:
        return "<p> FILL route </p>"
    except Exception as e:
        print("Erreur lors du remplissage de la base de données :", str(e))

@app.route('/transform', methods = ['GET']) # TODO: est-ce vraiment une méthode get ?
def transform():
    try:
        return "<p> TRANSFORM route </p>"
    except Exception as e:
        print("Erreur lors de la transformation en DataFrame :", str(e))


@app.route('/result', methods = ['POST'])
def result():
    try :
        song1 = request.form.get('song1')
        A1, T1 = song1.split(' - ')
        song2 = request.form.get('song2')
        A2, T2 = song2.split(' - ')
        song3 = request.form.get('song3')

        songs = Songs.query.all()

        if song3:
            A3, T3 = song3.split(' - ')
            # Verify that the songs are in the database :
            exist1 = Songs.query.filter_by(artist=A1, title=T1).first()
            exist2 = Songs.query.filter_by(artist=A2, title=T2).first()
            exist3 = Songs.query.filter_by(artist=A3, title=T3).first()
            if (exist1 is not None) and (exist2 is not None) and (exist3 is not None):
                #
                # code to analyse the preferencies
                #
                song_recomended1 = 'Camille - Le thé du matin'
                song_recomended2 = 'Camille - Le thé du matin'
                song_recomended3 = 'Camille - Le thé du matin'
                return render_template('result.html', reco1 = song_recomended1, reco2 = song_recomended2, reco3 = song_recomended3, songs = songs)
            else:
                flash('One of the songs that you choose is not into our database', 'danger')
                # Redirect to home page
                return redirect(url_for('home'))
        else:
            exist1 = Songs.query.filter_by(artist=A1, title=T1).first()
            exist2 = Songs.query.filter_by(artist=A2, title=T2).first()
            if (exist1 is not None) and (exist2 is not None):
                #
                # code to analyse the preferencies
                #
                song_recomended1 = 'Camille - Juste pour deux chansons'
                song_recomended2 = 'Camille - Juste pour deux chansons'
                song_recomended3 = 'Camille - Juste pour deux chansons'
                return render_template('result.html', reco1 = song_recomended1, reco2 = song_recomended2, reco3 = song_recomended3, songs = songs)
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
#Creer d'abord la db avec toutes les col (vérifier que oms dans le fill_db = noms dcol dans db) + l'appeler songs normalement sinon modifier dans le insert et dans la classe le nom de la table
# verifier que les mêmes noms de col dans db
def fill_db(pkl_file):
    try:
        with db.session.begin():
            for i in pkl_file.index:
                db.session.execute(
                    text("INSERT INTO songs (artist, title, album, lyrics, dim1, score1, dim2, score2, dim3, score3) VALUES (:artist, :title, :album, :lyrics, :dim1, :score1, :dim2, :score2, :dim3, :score3)"),
                    {"artist" : pkl_file["Artist"][i], 
                     "title" : pkl_file["Name "][i], 
                     "album" : pkl_file["Album"][i], 
                     "lyrics" : pkl_file["Lyrics"][i], 
                     "dim1" : pkl_file["Dimension 1"][i], 
                     "score1" : pkl_file["Score 1"][i], 
                     "dim2" : pkl_file["Dimension 2"][i], 
                     "score2" : pkl_file["Score 2"][i],  
                     "dim3" : pkl_file["Dim 3"][i],  
                     "score3" : pkl_file["Score 3"][i]
                    }
                )
    except Exception as e:
        print("Erreur dans le remplissage de la base de données:", str(e))
