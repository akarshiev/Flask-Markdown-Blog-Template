from flask import Blueprint, render_template, abort
from app.utils import get_all_posts, get_post_metadata

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    posts = get_all_posts()
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/post/<slug>')
def post_detail(slug):
    post = get_post_metadata(f"{slug}.md")
    if not post:
        abort(404)
    return render_template('blog/post.html', post=post)