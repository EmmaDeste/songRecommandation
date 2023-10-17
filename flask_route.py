from flask import Flask
from flask import Flask, render_template, request, jsonify, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Set the secret key
app.secret_key = 'DaTaCaMP'

################################################################ Configuration de la connexion à la base de données #################################################################
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projet_data_camp'

################################################################ Définition de l'URL de connexion à la base de données #################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}"

db = SQLAlchemy(app)

# Model for the songs table :
class Songs(db.Model):
    __tablename__ = 'songs'
    artist = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), primary_key=True, nullable=False)
    per_pos = db.Column(db.DECIMAL(5, 2), nullable=False)
    per_neg = db.Column(db.DECIMAL(5, 2), nullable=False)
    topic1 = db.Column(db.String(50), nullable=False)
    topic2 = db.Column(db.String(50), nullable=False)
    topic3 = db.Column(db.String(50), nullable=False)

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
                song_recomended = 'Camille - Le thé du matin'
                return render_template('result.html', reco = song_recomended, songs = songs)
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
                song_recomended = 'Camille - Juste pour deux chansons'
                return render_template('result.html', reco = song_recomended, songs = songs)
            else:
                flash('One of the songs that you choose is not into our database', 'danger')
                # Redirect to home page
                return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('An error occurred, please try again', 'danger')
        # Redirect to home page
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()