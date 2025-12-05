import os


class Config:
    # Bu kalitni har bir loyiha uchun o'zgartirish kerak.
    """
    import secrets
    secret_key = secrets.token_hex(16)
    print(secret_key)
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-and-fallback-secret-key'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    POSTS_FOLDER = os.path.join(BASE_DIR, 'posts')
    UPLOADS_FOLDER = os.path.join(BASE_DIR, 'app/static/uploads')

    # Bu shifrlangan parol. Uni yangi, kuchli parollar bilan almashtirish shart.
    # Hozirgi qiymat 'admin123' paroli. Yangi parol yaratish uchun hashlib.sha256("yangiparol".encode()).hexdigest() dan foydalaning.
    ADMIN_HASH = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'  # Default: admin123
