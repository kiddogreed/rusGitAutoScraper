# Rus Git Auto Scraper — Build Plan & Tracking Log

> **Project:** Rus Git Auto Scraper
> **Description:** Automated web scraper powered by GitHub Actions with a static dashboard hosted on GitHub Pages.

---

## 📋 Table of Contents
- [Phase 1: Project Setup & Repository Initialization](#phase-1-project-setup--repository-initialization)
- [Phase 2: Build the Core Web Scraper](#phase-2-build-the-core-web-scraper)
- [Phase 3: Build the Static User Interface (Frontend)](#phase-3-build-the-static-user-interface-frontend)
- [Phase 4: Setup GitHub Actions Automation](#phase-4-setup-github-actions-automation)
- [Phase 5: Enable GitHub Pages & Final Deployment](#phase-5-enable-github-pages--final-deployment)
- [Change Log & Tracking History](#change-log--tracking-history)

---

## Phase 1: Project Setup & Repository Initialization

### Objectives
- Establish the folder structure for **Rus Git Auto Scraper**.
- Initialize the Git repository and prepare dependencies.

### Steps for AI Agent:
1. Initialize the local directory structure:
   ```text
   rusGitAutoScraper/
   ├── .github/
   │   └── workflows/
   │       └── scrape.yml
   ├── scraper.py
   ├── index.html
   ├── requirements.txt
   └── BUILD_PLAN.md
   ```
2. Initialize a local Git repository (`git init`).
3. Add placeholder/stub implementations so later phases have a working
   foundation to build on:
   - `scraper.py` — entry point with a `scrape()`/`save()` stub that writes
     `data.json` (consumed by the dashboard).
   - `index.html` — static dashboard that fetches and renders `data.json`.
   - `requirements.txt` — base scraping dependencies (`requests`,
     `beautifulsoup4`, `lxml`).
   - `.github/workflows/scrape.yml` — scheduled GitHub Actions workflow that
     installs dependencies, runs the scraper, and commits updated data.

### Status: ✅ Done

---

## Phase 2: Build the Core Web Scraper

### Objectives
- Implement real scraping logic in `scraper.py` and produce a meaningful
  `data.json` for the dashboard.

### Decisions / Assumptions
`handover.md` did not specify a scrape target. Based on the project name
("Rus **Git** Auto Scraper") and user input during clarification, Phase 2
targets **GitHub's public Trending page** (`https://github.com/trending`),
which requires no authentication. If a different target was intended,
only `scraper.py`'s `Config`/`parse_trending()` need to change — the
workflow and dashboard contract (`data.json`) stay the same.

### What was built
- `scraper.py`:
  - `Config` — reads `TRENDING_LANGUAGE` (default: all languages) and
    `TRENDING_SINCE` (`daily`/`weekly`/`monthly`, default `daily`) env vars.
  - `fetch_html()` — fetches the trending page with a descriptive User-Agent.
  - `parse_trending()` — parses each `article.Box-row` into a dict with
    `rank`, `owner`, `name`, `full_name`, `url`, `description`, `language`,
    `stars_total`, `forks_total`, `stars_in_period`.
  - `scrape()`/`save()` — unchanged contract from Phase 1, now with real data.
- `.github/workflows/scrape.yml`:
  - Per clarification, triggers on **`workflow_dispatch` only** (manual
    runs) with `language` and `since` inputs mapped to the env vars above.
    The previous `schedule:`/`push:` triggers were removed; a cron schedule
    can be re-added later if automatic runs are wanted.
- Verified live: run against `github.com/trending` (default and with
  `language=python&since=weekly`) — correctly parsed real repos into
  `data.json`.

### Status: ✅ Done

## Phase 3: Build the Static User Interface (Frontend)
_Not started. `index.html` currently renders items generically
(`JSON.stringify`); will be upgraded to a proper dashboard layout for the
GitHub-trending schema from Phase 2._

## Phase 4: Setup GitHub Actions Automation
_Workflow trigger finalized in Phase 2 (manual `workflow_dispatch` only,
per clarification). No further automation changes planned unless scheduled
runs are requested._

## Phase 5: Enable GitHub Pages & Final Deployment
_Not started._

---

## Change Log & Tracking History

| Date | Phase | Change |
|------|-------|--------|
| 2026-10-29 | Phase 1 | Initialized git repo; created folder structure (`.github/workflows/`), `scraper.py`, `index.html`, `requirements.txt`, and this `BUILD_PLAN.md`. |
| 2026-10-29 | Phase 2 | Implemented GitHub Trending scraper in `scraper.py` (configurable via `TRENDING_LANGUAGE`/`TRENDING_SINCE`); updated `scrape.yml` to manual-only trigger with matching workflow inputs; verified live against github.com/trending. |
