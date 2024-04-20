from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class RecipesForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    picture = FileField('Картинка блюда')
    ingridients = TextAreaField("Ингридиенты", validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
