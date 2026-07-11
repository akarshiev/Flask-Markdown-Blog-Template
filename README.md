# Flask Markdown Blog & Portfolio Template

A minimalist, fast personal blog and portfolio built with **Flask**. Posts are
plain Markdown files — no database, no admin panel, no CMS. Deploys free on
Vercel in minutes. Personalize the entire site by editing a single config file.

> Live example: [abdukarim.uz](https://abdukarim.uz)

![Made with Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-e0a458)
![Deploy: Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?logo=vercel)

---

## Features

- **Markdown posts** — write in `.md`, the filename becomes the URL. No database.
- **One-file setup** — all personalization lives in `config.py`.
- **Dark, minimal design** — floating pill navbar, JetBrains Mono, amber accent.
- **Syntax highlighting** — fenced code blocks via Pygments.
- **Live GitHub projects** — the Building page pulls your public repos automatically.
- **Bookmarks** — a curated links page, editable via one JSON file.
- **Resume page** — embeds your PDF with a download button.
- **SEO built in** — meta tags, Open Graph, Twitter cards, JSON-LD, `sitemap.xml`, `robots.txt`.
- **Reading experience** — reading time, progress bar, copy-code buttons, share button.
- **Zero build step** — plain CSS, ships as-is. Deploys free on Vercel.

---

## Pages

| Route | What it is |
|---|---|
| `/` | Home — bio, avatar, social links |
| `/blogs` | List of all posts, newest first |
| `/blogs/<slug>` | A single article |
| `/building` | Your public GitHub repos, live |
| `/bookmarks` | Curated links with category filters |
| `/lectures` | Placeholder for videos (optional) |
| `/cv` | Embedded resume PDF + download |
| `/sitemap.xml`, `/robots.txt` | SEO, generated automatically |

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python wsgi.py
```

Open <http://localhost:5000>. That's it.

---

## Make it yours

Everything personal lives in **`config.py`**. Open it and edit the `SITE` and
`SOCIALS` sections:

```python
SITE = {
    "name":        "Your Name",
    "first_name":  "Your",
    "job_title":   "Software Developer",
    "domain":      "https://example.com",
    "bio_line_1":  "Developer building things on the web.",
    "github_username": "octocat",     # powers the /building page + avatar fallback
    ...
}

SOCIALS = [
    {"icon": "github",   "label": "GitHub",   "url": "https://github.com/octocat"},
    {"icon": "linkedin", "label": "LinkedIn", "url": "https://linkedin.com/in/you"},
    ...
]
```

Then replace three files with your own:

| File | What it is |
|---|---|
| `app/static/images/avatar.png` | Your profile photo (square) |
| `app/static/images/og-cover.png` | Social-share preview (1200×630) |
| `app/static/files/cv.pdf` | Your resume |

That's the whole personalization. No template editing required.

---

## Writing posts

Add a Markdown file to `posts/`. The filename is the URL slug — `posts/my-first-post.md`
becomes `/blogs/my-first-post`.

```markdown
title: My first post
date: 2026-01-15
summary: A short line used in previews and SEO.
tags: java, tutorial
image: https://example.com/cover.png

Your **Markdown** content starts here...
```

Only `title` and `date` are required. Dates accept `YYYY-MM-DD`, `DD-MM-YYYY`,
or `DD/MM/YYYY` — all normalized for the sitemap. See `posts/welcome.md` for a
full example. Delete the two sample posts when you're ready.

---

## Editing bookmarks

Edit `data/bookmarks.json`:

```json
[
  { "title": "Spring Boot Docs", "url": "https://...", "category": "Java" }
]
```

Categories become filter buttons automatically.

---

## Deploy to Vercel (free)

1. Push your repo to GitHub.
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your repo.
3. Vercel auto-detects `vercel.json`. Click **Deploy**.
4. Add your custom domain under **Settings → Domains** (optional).

To set a production secret key, add an environment variable `SECRET_KEY` in
Vercel's project settings (see `.env.example`).

### Google Search Console (optional)

To verify ownership, paste your verification token into `config.py`:

```python
"google_site_verification": "google1234567890abcdef",
```

The route `/google1234567890abcdef.html` is then served automatically. Submit
`https://yourdomain.com/sitemap.xml` in Search Console to get indexed faster.

---

## Project structure

```
config.py                 ← edit this to personalize everything
wsgi.py                   ← entry point
vercel.json               ← Vercel deploy config
requirements.txt
posts/                    ← your Markdown posts
data/bookmarks.json       ← your bookmarks
app/
├── __init__.py           ← app factory, loads config
├── utils.py              ← Markdown + front-matter parser
├── routes/__init__.py    ← all routes
├── static/
│   ├── css/style.css
│   ├── images/           ← avatar.png, og-cover.png
│   └── files/cv.pdf
└── templates/
    ├── base.html         ← shared layout, navbar, SEO
    ├── _icons.html       ← social icon SVGs
    ├── index.html        ← home
    ├── blog/             ← list + single post
    ├── bookmarks.html, building.html, lectures.html, resume.html
    └── 404.html
```

---

## Tech stack

- **Flask 3** — web framework
- **Python-Markdown** — post rendering
- **Pygments** — code syntax highlighting
- **Vanilla CSS + JS** — no build tooling
- **Gunicorn** — production WSGI server

---

## License

MIT — free to use, modify, and share. See [LICENSE](LICENSE).

If you build something with this, a link back to the original repo is
appreciated but not required. 🙂
