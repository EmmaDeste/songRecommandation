\\Super giga méga important : avant d'executer ce code, penser à bien SUPRIMER les fichiers et folder suivant :
- _pycache_ (dans le folder général et dans python_files)
- venv

\\ Démarer le server Flask :
python -m venv venv 
.\venv\Scripts\activate   \\ pour Mac : source venv/bin/activate

\\ Si pas déjà fait :
pip install flask
pip install flask-sqlalchemy
pip install pymysql
pip install cryptography

\\ pour lancer le server :
python -m flask --app .\flask_route.py run    \\ pour Mac : python -m flask --app flask_route:app run 

Ca marche ! ᕙ(⇀‸↼‶)ᕗ