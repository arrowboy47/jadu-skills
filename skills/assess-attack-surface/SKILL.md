---
name: assess-attack-surface
description: "Weekly passive attack-surface assessment of the homelab — enumerates current exposed ports/services on the Mac Mini and thebigbox, compares them against the documented baseline in server_monitoring_system/attacksurface.md and the Obsidian Infrastructure Index, and flags drift: new open ports, containers/services newly bound to 0.0.0.0, stopped/missing documented services, and regressed localhost binds. Passive only — never actively probes or scans. Fired weekly by the Hermes cron job weekly-attack-surface-assessment (Mon 08:00), delivers a severity-ranked summary to Telegram."
version: 1.0.0
author: jadu
platforms: [macos]
metadata:
  hermes:
    tags: [security, attack-surface, homelab, monitoring, passive]
    config:
      attacksurface.baseline: /Users/jadu/projects/server_monitoring_system/attacksurface.md
      attacksurface.infra_index: "/Users/jadu/Documents/Notes/Reference/Jadus references/Guides/Infrastructure Index.md"
---

# Assess Attack Surface

Weekly **passive** check of the homelab attack surface. Reads the documented baseline, enumerates what's actually listening/exposed right now on the Mac Mini and thebigbox, diffs the two, and reports drift. Fired unattended by the Hermes cron job `weekly-attack-surface-assessment` (`0 8 * * 1`, Mon 08:00), which delivers the final summary to Telegram.

**Scope of authorization.** All assets are owned/operated by Aiden for **defensive** purposes. This skill is **passive only** — read state, never send auth attempts, never run a scanner (nmap/nikto/etc.), never touch third-party vendors. Active testing of owned assets is proposed-and-approved only (see *Active mode* below).

## Hosts & baseline

| Host | Reach | Notes |
|------|-------|-------|
| **Mac Mini M4** | local (this host) | Hermes/Jadu server, Ollama, llama-server. Enumerate directly. |
| **thebigbox** | `ssh <bigbox-user>@<bigbox-lan-ip>` | ~28–30 Docker containers, ARR/media/memory. |
| MacBook Air M1 | `ssh jadu@<macbook-lan-ip>` (optional) | BlueBubbles `:1234` only — check if reachable, skip on timeout. |

Baseline lives in `attacksurface.md` (config `attacksurface.baseline`): §0 critical actions + remediation status, §1 hosts, §2 self-hosted services (per-service expected bind/exposure/auth), §7 testing schedule + Next-due dates. Current service map + ports live in the vault `Infrastructure Index.md` (config `attacksurface.infra_index`) and its per-service `Services/*.md` notes.

## How to run

### 1. Load the baseline
Read `attacksurface.md` — note especially §0 remediation status (what was *supposed* to be fixed, e.g. Jadu `:8000` → `127.0.0.1`, llama-server → `127.0.0.1:8080`, Ollama → `127.0.0.1:11434`) and §7 Next-due (passive) dates. Read `Infrastructure Index.md` for the expected running-service set. Only assess assets whose §7 Next-due (passive) is **due or overdue** relative to today; skip those not yet due.

### 2. Enumerate current exposure (passive)

**Mac Mini (local):**
```bash
# Non-localhost TCP listeners (0.0.0.0 / * / LAN IP = LAN-exposed)
lsof -nP -iTCP -sTCP:LISTEN | awk 'NR==1 || ($9 !~ /127\.0\.0\.1|\[::1\]/)'
```
Flag anything bound to `0.0.0.0`/`*`/`192.168.*` that the baseline says should be localhost.

**thebigbox (SSH):**
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 <bigbox-user>@<bigbox-lan-ip> \
  'echo "== containers =="; docker ps --format "{{.Names}}\t{{.Ports}}"; \
   echo "== stopped =="; docker ps -a --filter status=exited --format "{{.Names}}\t{{.Status}}"; \
   echo "== listeners =="; ss -tlnH'
```
In the `Ports` column, `0.0.0.0:<p>->` or `:::<p>->` = published to all interfaces; `127.0.0.1:<p>->` = localhost-only.

### 3. Diff against baseline → findings
Compare current state to the baseline and raise a finding for each of:
- **New open port** — a listening port / published container port not in the baseline §2/§5 or Infra Index.
- **New 0.0.0.0 bind** — a service published to all interfaces that the baseline expected on localhost, **or** a brand-new all-interfaces bind. Regression of a §0 remediation (Jadu/Ollama/llama-server back on `0.0.0.0`) is **at least 🟠**, flag prominently.
- **Stopped / missing service** — a documented service (Infra Index running set: ARR stack, qBittorrent, Jellyfin, Immich, Nextcloud, Honcho, CouchDB, Pi-hole, Nginx Proxy Manager, Homarr, etc.) not running / exited on bigbox, or a documented Mini listener gone.
- **Newly-public** — anything that flipped `LAN`→`PUBLIC` (e.g. a new DuckDNS/reverse-proxy forward). Do not test the forward from outside — note it and flag for confirmation.

Assign severity per the baseline legend: 🔴 Critical · 🟠 High · 🟡 Medium · 🟢 Low/Info. Weight by exposure × data/credential sensitivity × blast radius (baseline §7 model). An unauthenticated, all-interfaces service holding secrets or agent control = 🔴.

### 4. Maintain the baseline (non-destructive)
- Append a dated line to `attacksurface.md` §Changelog: `**<today>** — Passive assessment: <n> assets checked, <k> findings (<severities>). <one-line gist>.`
- For each asset assessed, set its §7 **Next-due (passive)** to `today + passive cadence` (cadence is in the same §7 row: Weekly / Bi-weekly / Monthly).
- Only add/adjust findings and dates. **Never** write a secret value into the file; if you ever see one there, redact + flag it (that's itself a 🔴). Never delete existing findings — mark resolved ones instead.

### 5. Report
Produce the summary as your **final response** — the cron runner delivers it to Telegram (do not send it yourself). Format:
- **Assets checked:** list.
- **New findings:** each as `<sev> <asset> — <what> (<where>) → <action>`, most-severe first.
- **Resolved / regressed:** since last baseline.
- **Next due:** updated dates.
- Lead with any new 🔴 critical on line one.

If nothing changed vs baseline and nothing is newly due, respond with exactly `[SILENT]` (nothing else) to suppress delivery.

## Active mode (approval-gated)
If a due asset genuinely warrants an **active** test (auth probe, TLS check, bind verification from off-host), **do not run it**. Post the proposed active-test plan (asset, exact commands, expected signal, blast radius) as your response and wait for manual approval — matches Hermes `approvals.mode: manual` / `cron_mode: deny`. Only Aiden's explicit go-ahead unlocks it, and only against §10 owned-asset targets. Third-party vendors are **config-review only — never scanned**.

## Rules
- **Passive by default.** Reading `lsof`/`ss`/`docker ps` over an existing SSH session is fine; sending traffic to a service to test its auth is *active* → approval-gated.
- Never scan or send credentials to third-party vendors (Anthropic, Google, Telegram, ATS portals, …).
- Never write secret values into `attacksurface.md` or any note — reference the file path only.
- If bigbox SSH fails: report thebigbox as **unreachable** (itself worth noting) and assess the Mini only; don't block the whole run.
- Exit criteria: a run is complete when every due asset is checked, findings recorded, §7 dates advanced, and the summary delivered (or `[SILENT]`).
