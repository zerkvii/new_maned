from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(40), nullable=False, default='user.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(64), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Integer, nullable=False, default=0)
    keyword = db.Column(db.String(64), nullable=True)
    post_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date}')"

    def get_category(self):
        dict = ['生活', '健康', '家庭', '管理', '旅行', '工作']
        return dict[self.category]

    def get_post_type(self):
        dict = ['视频', '声音', '相册', '文字']
        return dict[self.post_type]
