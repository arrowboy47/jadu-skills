#!/usr/bin/env python3
"""
Pre-run script for nightly-planner cron job.
Gathers vault context and injects it into the agent prompt.
Outputs to stdout — Hermes passes this as additional context.
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

VAULT = Path.home() / "Documents" / "Notes"
DAILY = VAULT / "Daily"
AREAS = VAULT / "Areas of Responsibility"


def read_safe(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def incomplete_tasks(text: str) -> list[str]:
    return [
        m.group(1).strip()
        for m in re.finditer(r"^- \[ \] (.+)$", text, re.MULTILINE)
    ]


def main():
    today = date.today()
    tomorrow = today + timedelta(days=1)

    today_note = read_safe(DAILY / f"{today.isoformat()}.md")
    tomorrow_note = read_safe(DAILY / f"{tomorrow.isoformat()}.md")
    morning = read_safe(AREAS / "Morning Routine.md")
    evening = read_safe(AREAS / "Evening Routine.md")
    future_raw = read_safe(AREAS / "Future Tasks.md")

    tasks_today = incomplete_tasks(today_note)
    future_tasks = incomplete_tasks(future_raw)

    print(f"=== NIGHTLY PLANNER CONTEXT ===")
    print(f"Today: {today.isoformat()}")
    print(f"Tomorrow: {tomorrow.isoformat()}")
    print()

    if tasks_today:
        print(f"INCOMPLETE TASKS FROM TODAY ({len(tasks_today)}):")
        for i, t in enumerate(tasks_today, 1):
            print(f"  {i}. {t}")
    else:
        print("INCOMPLETE TASKS FROM TODAY: none")
    print()

    if future_tasks:
        print(f"FUTURE TASKS AVAILABLE ({len(future_tasks)}):")
        for t in future_tasks:
            print(f"  - {t}")
    else:
        print("FUTURE TASKS AVAILABLE: none")
    print()

    print("MORNING ROUTINE:")
    print(morning.strip() if morning else "  (file not found)")
    print()

    print("EVENING ROUTINE:")
    print(evening.strip() if evening else "  (file not found)")
    print()

    if tomorrow_note:
        print("TOMORROW NOTE (pre-existing):")
        print(tomorrow_note.strip()[:500])
    else:
        print("TOMORROW NOTE: none (open slate)")


if __name__ == "__main__":
    main()
