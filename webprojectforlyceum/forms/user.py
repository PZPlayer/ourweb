from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    name = StringField('имя', validators=[DataRequired()])
    password = StringField('пароль', validators=[DataRequired()])
    password_again = StringField('подтверждение пароля', validators=[DataRequired()])
    
    submit = SubmitField('Войти')
    