from flask import Flask, render_template, redirect, request, make_response, session, flash
from data import db_session
from data.users import User
from data.recipe import Recipes
from sqlalchemy import or_
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.recipes import RecipesForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from data import db_session, NewsAPI
from werkzeug.utils import secure_filename
import uuid as uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_123'
login_manager = LoginManager()
login_manager.login_view = 'register'
login_manager.init_app(app)

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/homepage') # главная страница сайта
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        recipes = db_sess.query(Recipes).filter(
        (Recipes.user != current_user) | (Recipes.is_private != True))
    else:
        recipes = db_sess.query(Recipes).filter(Recipes.is_private != True)
    return render_template('home2.html', recipes=recipes)


@app.route('/register', methods=['GET', 'POST']) # страница регистрации
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not (form.name.data and form.email.data):
            flash('обязательно заполнить все поля', category='error')
        elif form.password.data != form.password_again.data:
            flash('пароли не совпадают', category='error')

        elif db_sess.query(User).filter(User.email == form.email.data).first():
            flash('такой пользователь уже существует', category='error')

        else:

            user = User(
                name=form.name.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            flash('аккаунт создан!', category='success')
            db_sess.add(user)
            db_sess.commit()
            login_user(user, remember=True)
            return redirect('/homepage')

    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST']) # просмотр профиля
@login_required
def profile():
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipes).filter((Recipes.user == current_user))
    return render_template('profile.html', user=current_user, recipes=recipes)


@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # picture = request.files['picture']
        # picture_filename = secure_filename(picture.filename)
        # unic_picture_filename = str(uuid.uuid1()) + '_' + picture_filename
        # form.picture.save(os.path.join(app.config['UPLOAD_FOLDER']), unic_picture_filename)
        recipe = Recipes(
            title=form.title.data,
            ingridients=form.ingridients.data,
            content=form.content.data,
            is_private=form.is_private.data
        )
        flash('Рецепт сохранён!', category='success')
        db_sess.add(recipe)
        db_sess.commit()
        return redirect('/profile')

    return render_template('add_recipe.html', form=form)


@app.route('/login', methods=['GET', 'POST'])  # страница входа
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('Вы успешно вошли', category='success')
            login_user(user, remember=True)
            return redirect("/")
        flash('Неверный пароль или почта', category='error')
    return render_template('login.html', form=form)


@app.route('/logout')  # выход из аккаунта
@login_required
def logout():
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    db_session.global_init("db/database2.db")
    app.register_blueprint(NewsAPI.blueprint)
    app.run(debug=True)
# from flask import Flask, render_template, request
#port=8080, host='127.0.0.1'
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('testReg.html')
#
# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form.get('username')
#     password = request.form.get('password')
#
#     with open('users.txt', 'a') as file:
#         file.write(f'Username: {username}, Password: {password}\n')
#
#     return 'Registration successful'
#
# if __name__ == '__main__':
#     app.run(debug=True)
