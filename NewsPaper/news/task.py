from datetime import datetime
from .models import Post


def task():
    post = Post.objects.filter(date=datetime.today())
    print(post)