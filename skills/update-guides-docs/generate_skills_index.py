#!/usr/bin/env python3
"""Generate the consolidated Obsidian note for INSTALLED (third-party) Hermes skills.
Numbered, green check = enabled, --- separators.

User-made skills (category `jadu/`, i.e. skills authored for this setup) are
EXCLUDED from the numbered catalog — each has its own dedicated note in
Guides/Skills/. This script instead emits a linked pointer section for them.
Rerun any time skills change; overwrites 'Hermes Skills Index.md'."""
import re, sys
from pathlib import Path
sys.path.insert(0, '/Users/jadu/.hermes/hermes-agent')
import yaml

SKILLS_ROOT = Path("/Users/jadu/.hermes/skills")
OUT = Path("/Users/jadu/Documents/Notes/Reference/Jadus references/Guides/Hermes Skills Index.md")
CFG = Path("/Users/jadu/.hermes/config.yaml")

# Skills under this category are user-authored → documented as individual notes,
# not listed in the consolidated catalog.
CUSTOM_CATEGORY = "jadu"

# Preserve correct capitalization for known acronyms in display titles.
ACRONYMS = {"pdw": "PDW", "jsms": "JSMS", "api": "API", "ai": "AI",
            "cli": "CLI", "sql": "SQL", "pdf": "PDF", "mcp": "MCP"}

disabled = set(yaml.safe_load(CFG.read_text())['skills']['disabled'])

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}
    out = {}
    for key in ("name", "description"):
        v = fm.get(key)
        if v is not None:
            out[key] = " ".join(str(v).split())
    return out

def title_case(slug):
    words = slug.replace("_", "-").split("-")
    return " ".join(ACRONYMS.get(w.lower(), w.capitalize()) for w in words)

def first_sentence(text):
    t = re.sub(r'^[\\"\'\s]+', '', text.strip())  # strip leading quotes/backslashes/space
    m = re.search(r"^(.*?[.!?])(\s|$)", t)
    return (m.group(1) if m else t).strip()

skills = []
for skill_md in sorted(SKILLS_ROOT.rglob("SKILL.md")):
    rel = skill_md.relative_to(SKILLS_ROOT)
    category = rel.parts[0] if len(rel.parts) > 1 else "(top-level)"
    slug = rel.parts[-2] if len(rel.parts) > 1 else rel.parts[0].removesuffix('.md') or category
    if len(rel.parts) == 1:
        slug = skill_md.parent.name if skill_md.parent != SKILLS_ROOT else slug
    fm = parse_frontmatter(skill_md.read_text(errors="replace"))
    name = fm.get("name", slug)
    desc = fm.get("description", "*No description in SKILL.md.*")
    skills.append((category, name, desc, str(skill_md.parent), name not in disabled))

skills.sort(key=lambda s: (s[0], s[1]))

custom  = [s for s in skills if s[0] == CUSTOM_CATEGORY]
catalog = [s for s in skills if s[0] != CUSTOM_CATEGORY]

n_installed = len(skills)
n_enabled   = sum(1 for s in skills if s[4])
n_catalog   = len(catalog)
n_custom    = len(custom)

lines = [f"""---
type: reference
topic: homelab
status: evergreen
date: 2026-07-15
tags:
  - reference
  - homelab
  - hermes-skill
  - self-hosted
---
# Hermes Skills Index

> [!summary]
> The **installed (third-party) skills** in the [[Hermes Agent]] at `~/.hermes/skills/` — {n_catalog} catalogued below, part of {n_installed} installed total (**{n_enabled} enabled** ✅ across all). Disabled state comes from `skills.disabled` in `~/.hermes/config.yaml`. Auto-generated from each skill's `SKILL.md` frontmatter — regenerate after skill changes per [[Documentation Maintenance]].

> [!note] User-made skills have their own notes
> The {n_custom} skills authored for this setup (`~/.hermes/skills/jadu/`) are **not** listed below — each has a dedicated note in `Guides/Skills/`, linked from [[Hermes Agent]]:"""]

for cat, name, desc, path, enabled in custom:
    lines.append(f"> - [[{title_case(name)}]] — {first_sentence(desc)}")

lines.append("")  # blank line after the callout

for i, (cat, name, desc, path, enabled) in enumerate(catalog, 1):
    check = " ✅" if enabled else ""
    lines.append(f"""
## {i}. {title_case(name)}{check}

**Category:** {cat}
**Skill:** `{name}` · **Path:** `{path}`

{desc}

---""")
lines.append(f"\n*{n_catalog} third-party skills catalogued · {n_custom} user-made (own notes) · {n_installed} installed · {n_enabled} enabled · generated from SKILL.md frontmatter.*\n")
OUT.write_text("\n".join(lines))
print(f"wrote {OUT.name}: {n_catalog} catalogued, {n_custom} custom (own notes), {n_installed} installed, {n_enabled} enabled")
