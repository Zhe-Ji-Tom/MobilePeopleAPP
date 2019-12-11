from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from . import app, db
from .models import User, Video, History
from .forms import LoginForm, RegistrationForm
import os

from flask_bootstrap import Bootstrap

bootstrap=Bootstrap(app)

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("home.html", title='Home Page', posts=posts)


@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        user_info = request.form.to_dict()
        user = User.query.filter_by(name=user_info.get("username")).first()
        if user is None or not user.check_password(user_info.get("password")):
            flash('Invalid username of password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_pate = url_for('home')
        return redirect(url_for('home'))
    return render_template('signin.html', title='Sign In')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        user_info = request.form.to_dict()
        check_user = User.query.filter_by(name=user_info.get("username")).first()
        if check_user is not None:
            flash("Username has existed")
            return redirect(url_for("register"))
        if user_info.get("password") != user_info.get("rpassword"):
            flash("Passwords are different")
            return redirect(url_for("register"))
        user = User(name=user_info.get("username"), email=user_info.get("email"), status=1, role_id=1)
        user.set_password(user_info.get("password"))
        check_user = User.query.filter_by(name=user_info.get("username")).first()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='signup')

@app.route('/home',methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='home')

@app.route('/account',methods=['GET', 'POST'])
def account():
    user = User.query.filter_by(name=current_user.__getattr__('name')).first()
    return render_template('account.html',user=user)


@app.route('/history',methods=['GET', 'POST'])
def history():
    user = User.query.filter_by(name=current_user.__getattr__('name')).first()
    histories = db.session.query(History, Video).filter(History.video_id == Video.id).filter_by(user_id=user.id, status=1).all()
    return render_template('history.html',histories=histories)

@app.route('/upload',methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        basePath = os.path.join(os.path.dirname(__file__), 'user')
        if not os.path.exists(basePath):
            print("yes")
    return render_template('upload.html',title='history')

@app.route('/reset',methods=['GET','POST'])
def reset():
    user = User.query.filter_by(name=current_user.__getattr__('name')).first()
    if request.method == "POST":
        user_info = request.form.to_dict()
        if user_info.get("password") == user_info.get("rpassword"):
            user.set_password(user_info.get("password"))
            db.session.commit()
            return render_template('account.html', user=user)
        else:
            flash('Passwords are different')
    return render_template('reset.html', user=user)

@app.route('/logout',methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == "POST":
        email_info = request.form.to_dict()
        user = User.query.filter_by(email=email_info.get("email")).first()
        if user:

            flash('Check your email for the instructions to reset your password')
            return render_template('signin.html', title='Sign In')
        else:
            flash('Please input a valid Email')
            return render_template('forget.html', title='Forget Password')
    else:
        return render_template('forget.html', title='Forget Password')

@app.route('/downloadVideo/<path:id>', methods=['GET', 'POST'])
def downloadVideo(id):
    videoLocation = db.session.query(Video.location).filter_by(id=id).first()
    r = requests.get(videoLocation[0])
    videoIO = BytesIO(r.content)
    return send_file(videoIO, as_attachment=True, attachment_filename='result.mp4', mimetype='video/mp4')


@app.route('/deleteVideo/<path:id>', methods=['GET', 'POST'])
def deleteVideo(id):
    history = History.query.filter_by(id=id).first()
    history.status = 0
    db.session.flush()
    db.session.commit()
    return redirect(url_for('retrieve_history'))