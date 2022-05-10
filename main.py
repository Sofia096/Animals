from flask import Flask, render_template, send_from_directory, redirect
import os
from data.reg_form import RegisterForm
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from data.login_form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def main_wind():
    db_session.global_init("db/animals.sqlite")
    return render_template('Title_page.html', title="Главная")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/regist', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('Registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('Registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('Registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        name = db_sess.query(User).filter(User.name == form.name.data).first()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if name and user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильная почта, пароль или имя",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/cat', methods=['GET', 'POST'])
def cat():
    return render_template('Cats.html', title='Меню кошки')


@app.route('/abisin', methods=['GET', 'POST'])
def abisin():
    return render_template('Abisin.html', title='Абиссинская кошка')


@app.route('/astro', methods=['GET', 'POST'])
def astro():
    return render_template('Astro.html', title='Австралийский мист')


if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(port=8080, host='127.0.0.1')
