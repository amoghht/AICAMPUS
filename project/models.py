from project import db,login_manager
from project import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

class user(db.Model,UserMixin):
    __tablename__ = 'user'
    id=db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    phone_number=db.Column(db.Integer(),nullable=False,unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash= db.Column(db.String(length=60), nullable=False)
    is_admin = db.Column(db.Integer(), nullable=False, default=0)
    addevents = db.Column(db.Integer(), nullable=False, default=0)
    events=db.relationship('events',backref='author',lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.password_hash =bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password )



class events(db.Model,UserMixin):
    event_id = db.Column(db.Integer(), primary_key=True)
    eventname = db.Column(db.String(length=30),nullable=False)
    eventcategory = db.Column(db.String(length=30), nullable=False)
    event_date = db.Column(db.String(20))
    event_description=db.Column(db.Text,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    register_link = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def get_id(self):
        return self.event_id



