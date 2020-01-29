from os import environ 

SECRET_KEY = environ.get('SECRET_KEY')
# API KEY not being used in this app
API_KEY = environ.get('API_KEY')
