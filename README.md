create new virtual environment: python3 -m venv venv
activate virtual environment: source ./venv/bin/activate
install Flask with help of pip: pip install Flask
save all requirements in txt file: pip freeze > requirements.txt
now I can run pip install -r requirements.txt in my own virtual env and all dependencies will be installed
for development: export FLASK_ENV=development
for defining start of script: export FLASK_APP=app.py
start the server: flask run