# how will the app work

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# define the database
db = SQLAlchemy()

# what happens when we create the app
def create_app():

    app = Flask(__name__)
    app.secret_key = "sloth"

    # import the blueprint that allows people to see things
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app