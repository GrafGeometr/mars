from flask import Flask
from data import db_session
from flask import render_template, redirect
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.jobs import JobForm
from flask import make_response
# from flask import session
from flask import request, abort
from flask import jsonify
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


"""@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.title = form.title.data
        job.content = form.content.data
        job.is_private = form.is_private.data
        current_user.news.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)"""

"""@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )
"""

"""@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')
"""


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    """if current_user.is_authenticated:
        news = db_sess.query(Jobs).filter(
            (Jobs.user == current_user) | (Jobs.is_private != True))
    else:
        news = db_sess.query(Jobs).filter(Jobs.is_private != True)"""
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", news=jobs)


def main():
    db_session.global_init("db/blogs.db")
    # app.register_blueprint(jobs_api.blueprint)
    app.run()
    """db_sess = db_session.create_session()


    user = User()
    user.surname = "Tober"
    user.name = "Cyret"
    user.age = 25
    user.position = "addec"
    user.speciality = "pilot"
    user.address = "roof_1"
    user.email = "noman@mars.org"
    user.hashed_password = "uuu"
    db_sess.add(user)

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scot_chief@mars.org"
    user.hashed_password = "haf"
    db_sess.add(user)

    user = User()
    user.surname = "Rutceg"
    user.name = "Foqeted"
    user.age = 18
    user.position = "elder helper"
    user.speciality = "engineer"
    user.address = "roof_2"
    user.email = "root@mars.org"
    user.hashed_password = "ufo"
    db_sess.add(user)

    user = User()
    user.surname = "Qefall"
    user.name = "Pattern"
    user.age = 23
    user.position = "fanf"
    user.speciality = "queue builder"
    user.address = "module_2"
    user.email = "queue@mars.org"
    user.hashed_password = "hfr"
    db_sess.add(user)

    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 5
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    db_sess.add(job)

    job = Jobs()
    job.team_leader = 2
    job.job = "finding water"
    job.work_size = 6
    job.collaborators = '4, 3'
    job.is_finished = False
    db_sess.add(job)

    db_sess.commit()

    print(123)"""

    '''user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "email1@email.ru"

    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.name = "Пользователь 2"
    user.about = "биография пользователя 2"
    user.email = "email2@email.ru"
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.name = "Пользователь 3"
    user.about = "биография пользователя 3"
    user.email = "email3@email.ru"
    db_sess.add(user)
    db_sess.commit()'''

    """user = db_sess.query(User).first()
    print(user.name)"""

    """for user in db_sess.query(User).all():
        print(user)

    for user in db_sess.query(User).filter(User.id > 1, User.email.notilike("%1%")):
        print(user)

    for user in db_sess.query(User).filter((User.id > 1) | (User.email.notilike("%1%"))):
        print(user)"""

    """news = News(title='Первая новость', content='Привет болгЁ',
                user_id=1, is_private=False)
    db_sess.add(news)
    db_sess.commit()

    user = db_sess.query(User).filter(User.id == 1).first()
    news = News(title="Вторая новость", content="Уже вторая запись!",
                user=user, is_private=False)
    db_sess.add(news)
    db_sess.commit()

    user = db_sess.query(User).filter(User.id == 1).first()
    news = News(title="Личная запись", content="Эта запись личная",
                is_private=True)
    user.news.append(news)
    db_sess.commit()

    for news in user.news:
        print(news)"""


"""@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res
"""

"""@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

"""

if __name__ == '__main__':
    main()
