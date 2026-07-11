"""
════════════════════════════════════════════════════════════════════════
  SITE CONFIGURATION  —  edit THIS file to make the blog yours.
════════════════════════════════════════════════════════════════════════

This is the only file you need to change to personalize the whole site:
your name, bio, social links, SEO metadata, and the GitHub username the
"Building" page pulls repositories from.

Everything below has sensible defaults. Change the values, save, redeploy.
"""

SITE = {
    # ── Identity ────────────────────────────────────────────────────────
    "name":        "Your Name",
    "first_name":  "Your",                       # used in "Hey, I'm Your."
    "job_title":   "Software Developer",
    "domain":      "https://example.com",        # your live URL, no trailing slash

    # ── Home page bio (two short lines under your name) ──────────────────
    "bio_line_1":  "Developer building things on the web.",
    "bio_line_2":  "I write about what I learn and keep my projects here.",

    # ── Avatar ──────────────────────────────────────────────────────────
    # Put your photo at app/static/images/avatar.png (square works best).
    # If that file is missing, this GitHub avatar is used as a fallback.
    "github_username": "octocat",                # also powers the /building page

    # ── SEO ─────────────────────────────────────────────────────────────
    "seo_description": "Personal blog and portfolio — articles and projects.",
    "seo_keywords":    "blog, portfolio, developer, projects",

    # Optional: education shown in the Person structured data (JSON-LD).
    # Leave name empty ("") to omit it entirely.
    "education": {
        "name":     "",                          # e.g. "MIT"
        "locality": "",                          # e.g. "Cambridge"
        "country":  "",                          # e.g. "US"
    },

    # Topics you know — shown in structured data, helps SEO.
    "knows_about": ["Programming", "Web Development"],

    # ── Resume / CV ─────────────────────────────────────────────────────
    # Put your PDF at app/static/files/cv.pdf
    "resume_download_name": "Your_Name_Resume.pdf",

    # ── Google Search Console verification (optional) ────────────────────
    # Paste the token from your google<...>.html verification file, or leave
    # empty to disable the route. Example: "google1234567890abcdef"
    "google_site_verification": "",
}


# ══════════════════════════════════════════════════════════════════════
#  SOCIAL LINKS
#  Order here = order shown on the home page. Delete any you don't use,
#  add any you want. Supported "icon" values (built-in SVGs):
#    github, linkedin, telegram, leetcode, substack,
#    twitter, instagram, youtube, email, website
#  For anything else, use "icon": "website" (a generic globe icon).
# ══════════════════════════════════════════════════════════════════════
SOCIALS = [
    {"icon": "github",   "label": "GitHub",   "url": "https://github.com/octocat"},
    {"icon": "linkedin", "label": "LinkedIn", "url": "https://linkedin.com/in/your-handle"},
    {"icon": "telegram", "label": "Telegram", "url": "https://t.me/your_handle"},
    {"icon": "email",    "label": "Email",    "url": "mailto:you@example.com"},
]
