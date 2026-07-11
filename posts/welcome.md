title: Welcome — how to write posts
date: 2026-01-01
summary: A quick guide to writing your own posts in this blog template.
tags: guide, getting-started

Welcome! If you can read this page, your blog is working. This post also
doubles as a mini-guide for writing your own.

## How posts work

Every post is a single Markdown file inside the `posts/` folder. The
filename becomes the URL slug — this file is `welcome.md`, so it lives at
`/blogs/welcome`. To publish a new post, just add a new `.md` file and
redeploy. No database, no admin panel.

## Front matter

The top of each file holds a few `key: value` lines:

```
title: Your post title
date: 2026-01-01
summary: One line shown in previews and used for SEO.
tags: java, backend, tutorial
image: https://example.com/cover.png
```

Only `title` and `date` really matter — the rest are optional. Dates can be
written as `2026-01-01`, `01-01-2026`, or `01/01/2026`; they're all
normalized automatically for the sitemap.

## Markdown works as you'd expect

You get **bold**, *italic*, [links](https://example.com), lists, quotes,
tables, and fenced code blocks with syntax highlighting:

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("world"))
```

> Blockquotes look like this — handy for callouts and key takeaways.

That's it. Delete this file whenever you're ready and start writing.
