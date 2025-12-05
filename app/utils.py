import os
import markdown
import datetime
from flask import current_app
from slugify import slugify


def get_post_metadata(filename):
    """
        Markdown fayl ichidan metadata (sarlavha, sana) va HTML kontentni ajratib oladi.

        Args:
            filename (str): O'qilishi kerak bo'lgan Markdown faylining nomi (masalan, 'post-slug.md').

        Returns:
            dict or None: Postning metama'lumotlari (title, date, slug, content, raw_content) yoki
                          agar fayl topilmasa None.
    """
    filepath = os.path.join(current_app.config['POSTS_FOLDER'], filename)

    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    md = markdown.Markdown(extensions=['meta', 'fenced_code', 'codehilite', 'tables'])
    html_content = md.convert(text)

    meta = md.Meta if hasattr(md, 'Meta') else {}

    return {
        'title': meta.get('title', [filename.replace('.md', '')])[0],
        'date': meta.get('date', [str(datetime.date.today())])[0],
        'slug': filename.replace('.md', ''),
        'content': html_content,
        'raw_content': text
    }


def get_all_posts():
    """
       Postlar papkasidagi barcha Markdown fayllarini topadi, metama'lumotlarni ajratadi
       va ularni sanasi bo'yicha saralab qaytaradi.

       Returns:
            list: Har bir postning metama'lumotlaridan iborat lug'atlar ro'yxati,
                eng yangisi birinchi o'rinda turadi.
    """
    files = os.listdir(current_app.config['POSTS_FOLDER'])
    posts = []

    for file in files:
        if file.endswith('.md'):
            post = get_post_metadata(file)
            if post:
                posts.append(post)

    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts


def save_post(title, content, current_slug=None):
    """
    Yangi postni fayl tizimiga yozadi yoki mavjud postni yangilaydi.
    Post faylning nomi sarlavhaga asoslangan slug yordamida yaratiladi.

    Args:
        title (str): Postning sarlavhasi.
        content (str): Postning Markdown matni.
        current_slug (str, optional): Agar post tahrirlanayotgan bo'lsa, mavjud slug.
                                      Agar o'zgarsa, eski fayl o'chiriladi. Defaults to None.

    Returns:
        str: Yaratilgan yoki yangilangan postning slug qiymati.
    """
    new_slug = slugify(title)

    if current_slug and current_slug != new_slug:
        delete_post_file(current_slug)

    filename = f"{new_slug}.md"
    filepath = os.path.join(current_app.config['POSTS_FOLDER'], filename)

    if os.path.exists(filepath):
        try:
            existing_meta = get_post_metadata(filename)
            date = existing_meta['date']
        except:
            date = datetime.date.today()
    else:
        date = datetime.date.today()

    file_content = f"""Title: {title}
Date: {date}

{content}
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)

    return new_slug


def delete_post_file(slug):
    """
        Berilgan slug'ga mos keluvchi Markdown faylini o'chiradi.

        Args:
            slug (str): O'chirilishi kerak bo'lgan postning slug'i.
        """
    filepath = os.path.join(current_app.config['POSTS_FOLDER'], f"{slug}.md")
    if os.path.exists(filepath):
        os.remove(filepath)
