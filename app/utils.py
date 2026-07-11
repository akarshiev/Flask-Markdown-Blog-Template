import os
import math
import markdown
import datetime
from flask import current_app


def _normalize_date(raw: str) -> str:
    """
    Normalize any date string to YYYY-MM-DD (ISO 8601 / Google sitemap spec).
    Handles: DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD, YYYY/MM/DD, DD.MM.YYYY.
    Returns the original string unchanged if no format matches.
    """
    raw = raw.strip()
    for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d', '%d.%m.%Y'):
        try:
            return datetime.datetime.strptime(raw, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return raw


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Parses simple key: value front matter at the top of the file.
    Supports multi-line values with indentation.
    Returns (meta_dict, body_text).
    """
    lines = text.splitlines()
    meta = {}
    body_start = 0

    for i, line in enumerate(lines):
        if i == 0 and line.strip() == '---':
            # YAML-fenced front matter
            for j in range(1, len(lines)):
                if lines[j].strip() == '---':
                    body_start = j + 1
                    for raw in lines[1:j]:
                        if ':' in raw:
                            k, _, v = raw.partition(':')
                            meta[k.strip().lower()] = v.strip()
                    break
            break
        if ':' in line and not line.startswith(' '):
            k, _, v = line.partition(':')
            meta[k.strip().lower()] = v.strip()
            body_start = i + 1
        else:
            break

    body = '\n'.join(lines[body_start:]).lstrip('\n')
    return meta, body


def get_post_metadata(filename: str) -> dict | None:
    posts_dir = current_app.config['POSTS_FOLDER']
    filepath = os.path.join(posts_dir, filename)
    if not os.path.exists(filepath):
        return None

    with open(filepath, encoding='utf-8') as f:
        raw = f.read()

    meta, body = _parse_frontmatter(raw)

    md = markdown.Markdown(
        extensions=['fenced_code', 'codehilite', 'tables', 'toc', 'nl2br'],
        extension_configs={'codehilite': {'css_class': 'highlight'}}
    )
    html = md.convert(body)

    slug = filename[:-3]  # strip .md
    date_str = _normalize_date(meta.get('date', str(datetime.date.today())))

    word_count = len(body.split())
    reading_minutes = max(1, math.ceil(word_count / 200))

    return {
        'slug': slug,
        'title': meta.get('title', slug.replace('-', ' ').title()),
        'date': date_str,
        'summary': meta.get('summary', ''),
        'tags': [t.strip() for t in meta.get('tags', '').split(',') if t.strip()],
        'image': meta.get('image', ''),
        'content': html,
        'reading_minutes': reading_minutes,
    }


def get_all_posts() -> list[dict]:
    posts_dir = current_app.config['POSTS_FOLDER']
    posts = []
    for fname in os.listdir(posts_dir):
        if fname.endswith('.md') and fname != '.gitkeep':
            p = get_post_metadata(fname)
            if p:
                posts.append(p)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts
