from flask import Flask, render_template


def create_app():
    """
        Flask ilovasini yaratish uchun Application Factory funksiyasi.
        Ilova sozlamalarini yuklaydi, Blueprints'larni ro'yxatdan o'tkazadi
        va xatoliklarni qayta ishlash handlerlarini sozlaydi.

        Returns:
            Flask: Konfiguratsiya qilingan Flask Application obyekti.
    """
    app = Flask(__name__)

    # Config faylidan sozlamalarni yuklash
    app.config.from_object('config.Config')

    # Blueprints (Routerlarni) ulash
    from app.routes.blog import blog_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)

    # 404 sahifa
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
