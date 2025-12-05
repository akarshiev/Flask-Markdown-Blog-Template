import hashlib
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash, abort
from werkzeug.utils import secure_filename
from app.utils import save_post, get_all_posts, delete_post_file, get_post_metadata

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def is_logged_in():
    return session.get('logged_in')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        if hashed_pw == current_app.config['ADMIN_HASH']:
            session['logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Parol noto'g'ri!")

    return render_template('auth/login.html')


@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


@admin_bp.route('/')
def dashboard():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    posts = get_all_posts()
    return render_template('admin/dashboard.html', posts=posts)


@admin_bp.route('/create', methods=['GET', 'POST'])
@admin_bp.route('/edit/<slug>', methods=['GET', 'POST'])
def edit(slug=None):
    if not is_logged_in(): return redirect(url_for('admin.login'))

    post = None
    if slug:
        post = get_post_metadata(f"{slug}.md")
        if not post: abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        save_post(title, content, current_slug=slug)
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create.html', post=post)


@admin_bp.route('/upload-image', methods=['POST'])
def upload_image():
    if not is_logged_in(): return {"error": "Unauthorized"}, 401

    uploaded_files = request.files.getlist('images')
    image_urls = []

    for file in uploaded_files:
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOADS_FOLDER'], filename))

            image_urls.append({
                'filename': filename,
                'url': url_for('static', filename=f"uploads/{filename}")
            })

    return {"status": "success", "images": image_urls}


@admin_bp.route('/delete/<slug>')
def delete(slug):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    delete_post_file(slug)
    return redirect(url_for('admin.dashboard'))
