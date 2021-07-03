from flask import Flask,abort,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from keras.models import load_model
import tensorflow as tf
import pickle

config=tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

app.config['SECRET_KEY']='c6045ea7d665c05be0d3e9ec'

db=SQLAlchemy(app=app)
bcrypt=Bcrypt(app=app)
login_manager=LoginManager(app=app)
login_manager.login_view="users.login_page"
login_manager.login_message_category='info'



encoder_model = 'project/models/facenet_keras.h5'
face_encoder = load_model(encoder_model)
def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict


from project.users.routes import users
from project.main.routes import main
from project.events.routes import events_bp

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(events_bp)


 
from project.models import user,events


admin=Admin(app=app)

class securemodelview(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return True
        else:
            abort(403)

admin.add_view(securemodelview(user,db.session))
admin.add_view(securemodelview(events,db.session))

