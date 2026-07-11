import os
import datetime
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.config['POSTS_FOLDER'] = 'posts'
    # Read the secret key from the environment in production; fall back to a
    # dev-only default so the app still runs locally with zero setup.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')

    # Load the user-facing site configuration (config.py in the project root).
    from config import SITE, SOCIALS

    # Make SITE and SOCIALS available in every template as {{ site }} / {{ socials }}
    @app.context_processor
    def inject_config():
        return {
            'site': SITE,
            'socials': SOCIALS,
            'current_year': datetime.date.today().year,
        }

    from app.routes.public import public_bp
    app.register_blueprint(public_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app
