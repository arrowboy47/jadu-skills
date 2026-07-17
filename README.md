# jadu-skills

Custom skills I wrote for my always-on personal agent ("Jadu"), built on [Nous Research hermes-agent](https://github.com/NousResearch/hermes-agent). A skill is a markdown playbook (`SKILL.md` with YAML frontmatter, agentskills.io-compatible) the agent loads on demand — optionally with helper scripts. These six run my daily automation, mostly on cron.

| Skill | Trigger | What it does |
|---|---|---|
| [nightly-planner](skills/nightly-planner/) | cron, 9:30pm daily | 12-phase evening planning session: gathers calendar/tasks/habit context (`scripts/gather_context.py`), negotiates tomorrow's plan over Telegram, writes the daily note + calendar events |
| [pdw-sync](skills/pdw-sync/) | cron 3am + on demand | Runs my [Personal Data Warehouse](https://github.com/arrowboy47/personal-data-warehouse) ETL — Obsidian notes + 5 Google Sheets → Postgres over SSH tunnel; Telegram alert on failure |
| [future-task-preprocessor](skills/future-task-preprocessor/) | cron, 4am daily | Turns raw ideas in my `Future Tasks` note into researched proposal docs (web research, options, recommendation) before I wake up |
| [assess-attack-surface](skills/assess-attack-surface/) | cron, Mon 8am | Passive attack-surface diff across my three home servers vs a living baseline doc; severity-ranked Telegram report. LAN details redacted in this copy |
| [add-blog-post](skills/add-blog-post/) | on demand | Publishes a post to my [website](https://github.com/arrowboy47/mywebsite) — writes the markdown, commits, pushes; Vercel auto-deploys |
| [update-guides-docs](skills/update-guides-docs/) | after any infra change | Keeps my Obsidian infrastructure docs (source of truth for every host/service/skill) in sync with reality, same conversation as the change |

## Why this design

The agent runtime stays narrow; capability lives at the edges as skills. Each skill is self-contained, versioned, and legible — the agent can read, follow, and improve them, and so can I. Deterministic steps live in scripts; judgment lives in the playbook prose.

These are copies of the live skills from `~/.hermes/skills/jadu/`, with network-identifying values replaced by placeholders.
