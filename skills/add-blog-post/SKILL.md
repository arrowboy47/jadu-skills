---
name: add-blog-post
description: "Add a new blog post to Aiden's personal website (github.com/arrowboy47/mywebsite, React/Vite on Vercel). Use when Aiden says 'write a blog post', 'post this to my blog', 'publish on my site', or wants website/blog updates. Covers drafting the markdown, images, build verification, and push-to-deploy."
version: 1.0.0
author: jadu
platforms: [macos]
metadata:
  hermes:
    tags: [blog, website, github, writing, publishing]
    config:
      website.repo_path: /Users/jadu/Projects/mywebsite
---

# Add Blog Post

Aiden's site is a React 19 + Vite + Tailwind app. Blog posts are plain markdown files auto-discovered by `src/utils/loadPosts.js` (`import.meta.glob` over `/src/posts/*.md`). Vercel auto-deploys `main` on push. GitHub auth: the `gh` CLI is already logged in as `arrowboy47` (shared `~/.config/gh`).

## Steps

1. **Pull latest** — `cd /Users/jadu/Projects/mywebsite && git pull`
2. **Read 2 recent posts** in `src/posts/` first — match Aiden's voice: first-person, practical, honest about what's unfinished, `##` section headings.
3. **Create the post** at `src/posts/<kebab-slug>.md`:

```markdown
---
title: "Post Title"
date: "YYYY-MM-DD"
description: "One-sentence hook shown in the blog list."
---

Body in markdown. ## for sections.
```

4. **Images** (optional): put files in `public/posts/`, reference as `![alt](/posts/filename.png)`.
5. **Verify build** — `npm run build` must exit 0 (catches bad frontmatter/markdown).
6. **Show Aiden the draft and get approval BEFORE pushing** — pushing = publishing live.
7. **Publish** — `git add -A && git commit -m "post: <title>" && git push` → Vercel deploys automatically, live in ~1 min.

## Related site edits (same repo, same flow)

- **Resume update**: drop new PDF in `src/assets/`, then update the import path in BOTH `src/HomePage.jsx` and `src/SideMenu.jsx` (search "Resume").
- **Projects page**: edit the hardcoded `projects` array in `src/ProjectsPage.jsx` (title, description, image, link).

## Hard rules

- Never push without Aiden's explicit OK on the content
- Always `npm run build` before pushing — broken build = broken live site
- Slug = filename = URL; don't rename published posts (breaks links)
- After any site change, update the `Personal Website` note in the Obsidian Guides folder per the `update-guides-docs` skill
