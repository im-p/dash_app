# dash_app

Dash application in virtual environment and heroku cloud

## instructions:

#### create virtualenv:
- virtualenv -p python3 env

#### activate virtualenv env:
- source env/bin/activate

#### make sure virtualenv and pip using python 3:
- pip --version && python --version

#### add app.py to folder, run the app to see what dependences are missing. Install using pip:
- pip install dash
- pip install pandas
- pip install fbprophet

#### install gunicorn to deploy python apps:
- pip install gunicorn

#### add requirements.txt:
- pip freeze > requirements.txt

#### add Procfile:
- web: gunicorn app:server

#### add runtime.txt:
- python-3.7.3

#### add .gitignore file:
- https://raw.githubusercontent.com/im-p/dash_app/master/.gitignore

#### git:
- git init
- git add -A
- git commit -m "deploying to heroku"

#### heroku:
- heroku login
- heroku create example-app
- git push heroku master
- heroku open

#### activate/deactivate dyno:
- heroku ps:scale web=1
- heroku ps:scale web=0

## Heroku:

### clone the repository:
- heroku login
- heroku git:clone -a hydrologiset-havainnot
 ### deploy changes:
- git add .
- git commit -am "make it better"
- git push heroku master
