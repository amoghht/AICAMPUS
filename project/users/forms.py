from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,DateField,SelectField,SelectMultipleField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError,URL
from project.models import user




class registrationform(FlaskForm):
    def validate_username(self,username_to_check):
        user_now=user.query.filter_by(username=username_to_check.data).first()
        if user_now:
            raise ValidationError("Username already exists! Please try a different username")
    def validate_email_address(self,email_address_to_check):
        email_address_now=user.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address_now:
            raise ValidationError("Email Address already exists! Please try a different Email Address")

    username = StringField(label='user name',validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='email address',validators=[Email(),DataRequired()])
    phone_number = IntegerField(label='phone number without country code', validators=[DataRequired()])
    password1=PasswordField(label='password',validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='confirm password',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='create account')

class loginform(FlaskForm):

    username = StringField(label='user name',validators=[DataRequired()])
    password=PasswordField(label='password',validators=[DataRequired()])
    submit=SubmitField(label='Sign In')
