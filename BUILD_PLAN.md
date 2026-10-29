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
_Not started. Requires target source(s) to scrape and the data schema to
collect before implementation can begin._

## Phase 3: Build the Static User Interface (Frontend)
_Not started. Will extend `index.html` once Phase 2 defines the real data
schema in `data.json`._

## Phase 4: Setup GitHub Actions Automation
_Scaffolded in Phase 1 (`.github/workflows/scrape.yml`); cadence/triggers may
be revisited once Phase 2 defines real runtime/rate-limit needs._

## Phase 5: Enable GitHub Pages & Final Deployment
_Not started._

---

## Change Log & Tracking History

| Date | Phase | Change |
|------|-------|--------|
| 2026-10-29 | Phase 1 | Initialized git repo; created folder structure (`.github/workflows/`), `scraper.py`, `index.html`, `requirements.txt`, and this `BUILD_PLAN.md`. |
