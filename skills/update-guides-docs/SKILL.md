---
name: update-guides-docs
description: "After ANY change to the application/AI stack (service added/removed/reconfigured, hermes skill or cron change, model/provider swap, new project, hardware/network change) — update the matching reference note in the Obsidian Guides folder in the same conversation. Also use when Aiden says 'document this' about infrastructure."
version: 1.0.0
author: jadu
platforms: [macos]
metadata:
  hermes:
    tags: [documentation, obsidian, homelab, infrastructure, maintenance]
    config:
      guides.path: /Users/jadu/Documents/Notes/Reference/Jadus references/Guides
---

# Update Guides Docs

The Guides folder is the source of truth for the whole stack — for Aiden, for Claude Code, and for you. **Every infra change you make or observe gets reflected there immediately, in the same conversation as the change.** Never let the docs drift.

Canonical procedure lives in the vault note `Documentation Maintenance.md` inside the Guides folder — read it before writing. Summary:

## Steps

1. Read `Infrastructure Index.md` at `/Users/jadu/Documents/Notes/Reference/Jadus references/Guides/` to locate the affected note:
   - services → `Services/<Name>.md` · hosts → `Hosts/` · projects → `Projects/`
   - **installed third-party skills** → ONE consolidated file `Hermes Skills Index.md` (regenerate: `python3 <skill_dir>/generate_skills_index.py` — numbered, ✅ = enabled; user-made `jadu/` skills are auto-excluded)
   - **user-made skills** (`~/.hermes/skills/jadu/`) → one hand-authored note each in `Guides/Skills/`. New `jadu/` skill = create its note (service-note pattern) + link it from `Hermes Agent.md` and `Infrastructure Index.md`
2. Apply the change:
   - **Modified** → update changed facts (ports, compose path, config, status), bump `date:` in frontmatter
   - **New** → create note using the service pattern in `Documentation Maintenance.md`
   - **Removed** → keep the note, mark removal date + where data was retained; move index entry to the *Removed* line
3. Update `Infrastructure Index.md` if anything was added/removed/recategorized.
4. Style rules (from `Reference/obsidian/vault guide.md`): frontmatter `type/topic/status/tags` required, H1 = filename, `[[wikilinks]]` for internal references, callouts for open questions.

## Hard rules

- **Never copy secrets** (tokens, session keys, passwords from compose/env files) into vault notes — reference the file path instead
- Never delete a note or its content — mark things removed/dormant instead
- One note per service; sidecar containers (db/redis) belong inside the parent service's note
- If you changed a hermes skill or its enabled state, also note the new enabled count in `Hermes Agent.md`
