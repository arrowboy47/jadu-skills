---
name: future-task-preprocessor
description: "Future-task preprocessor — reads Aiden's Obsidian Future Tasks list, picks (or is told) an unchecked task, researches it, and writes a proposed-solution markdown file into the vault. Runs nightly via cron and on demand as /future-task-preprocessor with optional quoted task text or #tag."
version: 1.0.0
author: jadu
platforms: [macos]
metadata:
  hermes:
    tags: [obsidian, planning, tasks, research]
    config:
      tasks.file: "/Users/jadu/Documents/Notes/Reference/Jadus references/Future Tasks.md"
      solutions.dir: "/Users/jadu/Documents/Notes/Reference/Jadus references/proposed solutions"
---

# Future Task Preprocessor

Turn one unchecked item from `Future Tasks.md` into a concrete proposed solution, saved as a markdown file in the vault's `proposed solutions` directory. Two modes — detect which one you're in:

- **Cron mode** (no user in the loop, scheduled run): pick a task yourself, do the full pipeline, report via the job's telegram delivery. Never ask questions.
- **Manual mode** (Aiden invoked the skill in chat, possibly with quoted text or a `#tag`): interpret which task he means, **confirm with him before doing the work**, then produce the plan.

## Paths

- Tasks file: `/Users/jadu/Documents/Notes/Reference/Jadus references/Future Tasks.md`
- Output dir: `/Users/jadu/Documents/Notes/Reference/Jadus references/proposed solutions/`

## Pipeline

### 1. Parse the tasks file

Unchecked tasks are lines matching `- [ ]` with non-empty text (skip blank `- [ ]` lines). Note each task's section heading (`## Learning`, `## Projects`, …) and any `#tags`.

### 2. Select a task

**Cron mode:**
- List existing files in the output dir. A task already has a solution if a file's frontmatter `task:` field (or filename slug) matches it — skip those.
- From the remaining unchecked tasks, pick **one**: prefer tasks that benefit from research/design (technical, homelab, project planning) over pure calendar items ("call X", "hang out with Y"). Skip personal errands entirely — they don't need a solution document.
- If no eligible task remains: deliver exactly a short "Nothing to do — no unchecked tasks needing a proposed solution." message and stop. Write no file.

**Manual mode:**
- If Aiden passed quoted text: fuzzy-match it against unchecked task lines.
- If he passed a `#tag`: list the unchecked tasks carrying that tag and ask which one (or if only one, confirm it).
- If no argument: show a short numbered list of eligible unchecked tasks and ask which one.
- **Always confirm the exact task line with him before researching.** After confirmation, proceed.

### 3. Research & propose

Investigate properly — web search where useful, check the local machine/homelab context where relevant (existing services, Docker stack, vault notes). Produce a real proposal, not a restatement: recommended approach, alternatives considered, concrete steps, tools/costs, open questions for Aiden.

**Research strategy (priority order):**
1. **Web search** via `web_search` (fast, for general info)
2. **Fallback to browser** via `browser_navigate` when web_search fails (e.g., FIRECRAWL_API_KEY not configured) — visit official docs directly
3. **Visual inspection** via `browser_vision` with `annotate=true` for complex UIs (dashboards, config panels)
4. **Local context** via `read_file`/`terminal` to check existing services, Docker containers, vault notes

### 4. Write the solution file

Create `proposed solutions/<kebab-slug-of-task>.md`:

```markdown
---
task: "<exact task line text, without the checkbox>"
source: "Future Tasks.md"
section: "<section heading>"
proposed: <YYYY-MM-DD>
status: proposed
---

# <Task title>

## Recommendation
<the proposed solution, one paragraph>

## Plan
<numbered concrete steps>

## Alternatives considered
<brief>

## Open questions
<things only Aiden can decide>
```

If a file for that slug already exists, don't overwrite — append `-v2` (then `-v3`, …).

### 5. Link in Future Tasks file

Append an Obsidian link to the new solution file at the end of the corresponding task line in `Future Tasks.md`. 
Example: `- [ ] Task text #tag [[proposed solutions/task-slug]]`

### 6. Notify

**Cron mode:** the job delivers to telegram — end your reply with a short summary: which task, the one-line recommendation, and the file path. If nothing to do, say only that.

**Manual mode:** reply in chat with the summary and file path.

## Rules

- Never check off, edit, or reorder anything in `Future Tasks.md`. Read-only.
- One task per cron run. Manual mode: one task per invocation unless Aiden asks for more.
- Solution files live only in the `proposed solutions` dir — never elsewhere in the vault.
- Cron mode must never block on a question; when genuinely ambiguous, pick the most research-worthy task and note the ambiguity in the file's Open questions.
