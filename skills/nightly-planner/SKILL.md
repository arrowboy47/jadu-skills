---
name: nightly-planner
description: \"Jadu's 12-phase evening planning session. Builds a time-blocked daily plan for tomorrow from calendar, tasks, routines, and open-ended goals.\"
version: 1.3.0
author: jadu
platforms: [macos]
metadata:
  hermes:
    tags: [planning, daily, obsidian]
    config:
      nightly_planner.vault_path: ~/Documents/Notes
      nightly_planner.timezone: America/Los_Angeles
---

# Nightly Planner

Jadu's evening planning session. Runs at 9:30 PM or when triggered manually.
Guides Aiden through a 12-phase workflow to build tomorrow's time-blocked schedule.

## Vault Paths (absolute, use these exactly)
- Morning Routine: /Users/jadu/Documents/Notes/Reference/Jadus references/Daily Routines.md
- Evening Routine: /Users/jadu/Documents/Notes/Reference/Jadus references/Daily Routines.md
- Future Tasks: /Users/jadu/Documents/Notes/Reference/Jadus references/Future Tasks.md
- Short Term Memory: /Users/jadu/Documents/Notes/Reference/Jadus references/Short Term Memory.md
- Today's note: /Users/jadu/Documents/Notes/Daily/[TODAY].md
- Tomorrow's note: /Users/jadu/Documents/Notes/Daily/[TOMORROW].md

## Phase 1 — Trigger

Send: \"Hey AK — time to plan tomorrow. Say READY when you want to start.\"
Wait for exact `READY` (case-sensitive). Do NOT proceed until received.

**Critical Timezone Anchor:**
Always confirm the current date and time in PST with the user before proceeding. Do not rely solely on the system clock (which may be UTC), as this causes \"tomorrow\" to shift prematurely if the session crosses midnight. Establish a hard date anchor (e.g., \"Today is Wednesday, July 8th\") before generating any file paths or calendar events. If the user corrects the date, update the anchor immediately and use the corrected date for all subsequent file paths.

If no response in 15 min, resend. Give up after 3 tries (45 min total).

## Phase 2 — Day Review

Ask: \"How was your day? What went well, what was rough, how are you feeling?\"
Write response verbatim to today's note under `## Day Review`. If the file exists, you MUST use a method that preserves existing content (e.g., read the file first and prepend/append, or use a patch tool) rather than overwriting the entire file with `write_file`.

## Phase 3 — Context Gathering

Read these files using read_file (absolute paths):
1. /Users/jadu/Documents/Notes/Reference/Jadus references/Daily Routines.md
2. /Users/jadu/Documents/Notes/Daily/[TODAY].md — extract incomplete tasks (lines matching `- [ ] `)
3. /Users/jadu/Documents/Notes/Reference/Jadus references/Future Tasks.md
4. /Users/jadu/Documents/Notes/Reference/Jadus references/Short Term Memory.md
5. /Users/jadu/Documents/Notes/Daily/[TOMORROW].md — if exists

Then send a 3-5 line summary: \"Here's what I've got for tomorrow: [key facts].\"

## Phase 4 — Incomplete Tasks & Tomorrow's Sheet

Explicitly tell the user: \"I'm now checking incomplete tasks from today to add to tomorrow's daily sheet.\"

List incomplete tasks from today's note.
If none: \"No incomplete tasks from today to roll over.\" → skip to Phase 5.
If tasks: ask \"Incomplete from today: [list]. Keep all, rollover some, or drop? Reply: 'keep all', 'rollover: 1,2', or 'drop all'.\"

## Phase 5 — Future Tasks

Read /Users/jadu/Documents/Notes/Reference/Jadus references/Future Tasks.md AND /Users/jadu/Documents/Notes/Reference/Jadus references/Short Term Memory.md.
If both are empty: \"Nothing in future or short-term tasks.\"
If tasks: show list from both files.

Ask: \"Anything to tackle tomorrow? Any additional tasks you want to accomplish? Reply with names or 'none'.\"

## Phase 6 — Routine Preview & Daily Tasks

Show morning and evening routine contents from Daily Routines.md (already read in Phase 3).
Determine the tasks for the day based on the contents of /Users/jadu/Documents/Notes/Reference/Jadus references/Daily Routines.md. These tasks are distinct from calendar events, though some (like gym) may overlap.

Ask: \"Sticking to these tomorrow or any changes? Also, any additional tasks you want to add to the list?\"

## Phase 7 — Open-Ended Goals

Ask: \"What else do you want to accomplish tomorrow? Include time estimates — e.g. 'Azure report (2 hrs)', 'Hindi (30 min)'.\"

Extract tasks. Assign labels:
- #work — work tasks
- #money — side hustles
- #wellness — gym, health
- #routine — daily habits
- #learning — Hindi, Spanish, data science
- #personal — personal life
- #homelab — Docker, servers, infra
- #randtodo — catch-all

If input too vague: ask ONE clarifying question. One attempt only, then proceed.

## Phase 8 — Schedule Proposal

Propose time-blocked schedule. Fixed blocks (do not move):
- Morning Routine: 6:30 AM – 8:30 AM
- Work: 8:30 AM – 5:30 PM
- Evening Routine: 8:00 PM – 10:30 PM

Incorporate ALL applicable daily tasks from the `Daily Routines.md` file (e.g., brushing teeth, coffee, Duolingo) into the schedule, even if repetitive. Use the time estimates provided in that file to determine how they fit into the available windows. Then, fit all other tasks in free windows. Show time estimates inline.
Flag tasks that don't fit: \"Couldn't fit: [task]\"
End with: \"Good to go? Reply CONFIRM to finalize.\"

Allow 2 revision requests. On 3rd: \"That's your 2 changes, Husk. CONFIRM to lock in or RESTART to redo from Phase 7.\"

## Phase 9 — Conflict Check

Use the `google-workspace` skill to list tomorrow's calendar events.
Check for overlaps with the proposed schedule.
If conflicts exist, report them and ask if the user wants to adjust the schedule.
If no conflicts: \"No calendar conflicts. Finalizing...\"

## Phase 10 — Write Daily Note

Write tomorrow's note to /Users/jadu/Documents/Notes/Daily/[TOMORROW].md using write_file.

Format:
```
---
type: daily
status: growing
topic: to-do
tags:
  - daily
---
# YYYY-MM-DD

## Day Review
[to be filled during evening planning]

## Tomorrow's Schedule
[full time-blocked schedule]

## Tasks
- [ ] Task name (X hrs) #label

## Notes

```

If file exists: merge — overwrite Schedule and Tasks sections, preserve everything else.
If file does not exist: create from scratch.

## Phase 11 — Calendar Events

Using the `google-workspace` skill, create calendar events for the confirmed time-blocked schedule.
- Use high-level block names (e.g., \"Morning Routine\", \"Work\", \"Evening Routine\") for the event summaries to keep the calendar clean.
- Ensure ISO 8601 format with correct timezone.
- **Execution Detail**: Use the `google_api.py` script via the terminal tool. Use the absolute path: `/Users/jadu/.hermes/skills/productivity/google-workspace/scripts/google_api.py`.
- **Critical**: Ensure the script is run using the agent's virtualenv Python (e.g., `/Users/jadu/.hermes/hermes-agent/venv/bin/python3`) to avoid `ModuleNotFoundError` for `googleapiclient`.
- **Argument Format**: The `create` action requires explicit flags: `--summary "Name" --start "ISO_TIMESTAMP" --end "ISO_TIMESTAMP"`. Do not pass these as positional arguments.
- **Formatting**: Timestamps MUST include the timezone offset (e.g., `2026-07-09T06:30:00-07:00`) or the API will return a 400 error.
Note: \"Calendar events created successfully.\"

## Phase 12 — Confirmation

Send: \"Done, AK. Daily note written and calendar updated for [date]. [N] tasks ready to track. Morning starts 6:30 AM. Get some sleep.\"

---

## Session Pause / Resume

If Aiden goes silent 10+ min:
- Send reminder every 15 min, up to 3 times
- On resume: \"Welcome back. We were on phase [N] — [one-line recap]. Let's keep going.\"
- Abandon at 7 AM if no response

## Task Format

`- [ ] Task name (X hrs) #label`
Rollover tasks: `- [ ] Task name #rollover`

## Tool Rules

Use ONLY read_file and write_file for Obsidian. For Calendar, use the google-workspace skill.
All paths are absolute: /Users/jadu/Documents/Notes/...
Ask one thing at a time. Wait for reply. Proceed.
