from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user
from app import app, bcrypt, db
from .forms import RegistrationForm, LoginForm
from .models import User, Post
import random
from utils import get_specified_post


@app.route('/')
@app.route('/index')
def index():
    headline = Post.query.all()[0]
    list_size = len(Post.query.all())
    fir = random.randint(2, list_size)
    sec = random.randint(2, fir)
    entries = [get_specified_post(fir), get_specified_post(sec)]
    return render_template('main/index.html', title='主页', headline=headline,
                           entries=entries)


@app.route('/account')
def account():
    return render_template('main/account.html', title='账户')


@app.route('/about')
def about():
    return render_template('main/about.html', title='关于')


@app.route('/contact')
def contact():
    return render_template('main/contact.html', title='联系')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'成功创建账户{form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='注册', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data.encode('utf-8')):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('登录失败，请检查账号或者密码', 'warn')
    return render_template('auth/login.html', title='登录', form=form)


@app.route('/posts/videos')
def video_posts():
    return render_template('posts/video_posts.html', title='视频博客')


@app.route('/posts/audios')
def audio_posts():
    return render_template('posts/audio_posts.html', title='音频博客')


@app.route('/posts/photos')
def photo_posts():
    return render_template('posts/photo_posts.html', title='照片博客')


@app.route('/posts/words')
def word_posts():
    return render_template('posts/word_posts.html', title='文字博客')


@app.route('/categories/life')
def life():
    return render_template('categories/life.html', title='生活')


@app.route('/categories/health')
def health():
    return render_template('categories/health.html', title='健康')


@app.route('/categories/family')
def family():
    return render_template('categories/family.html', title='家庭')


@app.route('/categories/manage')
def manage():
    return render_template('categories/manage.html', title='管理')


@app.route('/categories/travel')
def travel():
    return render_template('categories/travel.html', title='旅行')


@app.route('/categories/work')
def work():
    return render_template('categories/work.html', title='工作')
