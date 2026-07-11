import json
import time
import os
import urllib.request
from flask import Blueprint, render_template, abort, send_from_directory, \
                  current_app, Response

from config import SITE

public_bp = Blueprint('public', __name__)

# ── GitHub live fetch (1-hour in-process cache) ──────────────────────────────
_gh_cache = {'data': None, 'ts': 0}
_GH_TTL   = 3600
_GH_USER  = SITE.get('github_username', 'octocat')

def _fetch_github_repos():
    now = time.time()
    if _gh_cache['data'] is not None and now - _gh_cache['ts'] < _GH_TTL:
        return _gh_cache['data']

    url = (f'https://api.github.com/users/{_GH_USER}/repos'
           '?type=public&sort=updated&per_page=30')
    req = urllib.request.Request(
        url, headers={'User-Agent': 'flask-blog-template/1.0',
                      'Accept': 'application/vnd.github+json'})
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            repos = json.loads(resp.read())
            filtered = [
                {
                    'name':        r['name'],
                    'description': r.get('description') or '',
                    'url':         r['html_url'],
                    'language':    r.get('language') or '',
                    'stars':       r.get('stargazers_count', 0),
                    'updated':     r.get('updated_at', '')[:10],
                    'fork':        r.get('fork', False),
                }
                for r in repos
                if not r.get('fork')
            ]
            _gh_cache['data'] = filtered
            _gh_cache['ts']   = now
            return filtered
    except Exception as exc:
        print(f'[github] fetch failed: {exc}')
        return _gh_cache['data'] or []


# ── Bookmarks from JSON ───────────────────────────────────────────────────────
def _load_bookmarks():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'bookmarks.json'))
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


# ── Routes ───────────────────────────────────────────────────────────────────
from app.utils import get_all_posts, get_post_metadata

@public_bp.route('/')
def index():
    return render_template('index.html')


@public_bp.route('/blogs')
def blogs_list():
    posts = get_all_posts()
    return render_template('blog/index.html', posts=posts)


@public_bp.route('/blogs/<slug>')
def blog_detail(slug):
    post = get_post_metadata(f'{slug}.md')
    if not post:
        abort(404)
    return render_template('blog/post.html', post=post)


@public_bp.route('/bookmarks')
def bookmarks():
    bms        = _load_bookmarks()
    categories = sorted(set(b['category'] for b in bms))
    return render_template('bookmarks.html', bookmarks=bms, categories=categories)


@public_bp.route('/building')
def building():
    repos = _fetch_github_repos()
    return render_template('building.html', repos=repos)


@public_bp.route('/lectures')
def lectures():
    return render_template('lectures.html')


@public_bp.route('/cv')
def cv():
    return render_template('resume.html')


@public_bp.route('/cv/download')
def cv_download():
    files_dir = os.path.join(current_app.root_path, 'static', 'files')
    return send_from_directory(
        files_dir, 'cv.pdf',
        as_attachment=True,
        download_name=SITE.get('resume_download_name', 'Resume.pdf')
    )


# ── SEO: sitemap.xml ─────────────────────────────────────────────────────────
@public_bp.route('/sitemap.xml')
def sitemap():
    base  = SITE.get('domain', '').rstrip('/')
    posts = get_all_posts()

    static_pages = [
        ('/',           '1.0', 'monthly'),
        ('/blogs',      '0.9', 'weekly'),
        ('/building',   '0.8', 'monthly'),
        ('/bookmarks',  '0.6', 'monthly'),
        ('/lectures',   '0.5', 'monthly'),
        ('/cv',         '0.7', 'monthly'),
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, priority, freq in static_pages:
        xml.append(f'  <url>')
        xml.append(f'    <loc>{base}{path}</loc>')
        xml.append(f'    <changefreq>{freq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append(f'  </url>')

    for post in posts:
        xml.append(f'  <url>')
        xml.append(f'    <loc>{base}/blogs/{post["slug"]}</loc>')
        xml.append(f'    <lastmod>{post["date"]}</lastmod>')
        xml.append(f'    <changefreq>never</changefreq>')
        xml.append(f'    <priority>0.8</priority>')
        xml.append(f'  </url>')

    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')


# ── SEO: robots.txt ──────────────────────────────────────────────────────────
@public_bp.route('/robots.txt')
def robots():
    base = SITE.get('domain', '').rstrip('/')
    content = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /cv/download\n'
        '\n'
        f'Sitemap: {base}/sitemap.xml\n'
    )
    return Response(content, mimetype='text/plain')


# ── Google Search Console verification (optional) ────────────────────────────
# Only registered if a token is set in config.py. The route serves the file
# Google expects at /<token>.html with the required body.
_gsv = SITE.get('google_site_verification', '').strip()
if _gsv:
    @public_bp.route(f'/{_gsv}.html')
    def google_verify():
        return Response(f'google-site-verification: {_gsv}',
                        mimetype='text/html')
