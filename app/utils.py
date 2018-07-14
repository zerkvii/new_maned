from app import db
from app.models import Post, User


def get_specified_post(num):
    return Post.query.filter_by(id=num).all()[0]


def capture_shotcut(link):
    return link
