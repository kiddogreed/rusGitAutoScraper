"""
Rus Git Auto Scraper
=====================
Phase 2: Core scraper implementation.

Scrapes GitHub's public "Trending" page (https://github.com/trending) and
collects the currently trending repositories into `data.json`, which the
static dashboard (index.html) reads and renders. No GitHub authentication
is required since the trending page is public HTML.

Configure what to scrape via environment variables (also exposed as
`workflow_dispatch` inputs in `.github/workflows/scrape.yml`):
  - TRENDING_LANGUAGE: language filter, e.g. "python" (empty = all languages)
  - TRENDING_SINCE: "daily" (default), "weekly", or "monthly"
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = Path(__file__).parent / "data.json"
TRENDING_BASE_URL = "https://github.com/trending"
REQUEST_TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (compatible; RusGitAutoScraper/1.0; +https://github.com/) "
    "python-requests"
)


@dataclass
class Config:
    """Scraper configuration, overridable via environment variables."""

    language: str = field(
        default_factory=lambda: os.environ.get("TRENDING_LANGUAGE", "").strip()
    )
    since: str = field(
        default_factory=lambda: os.environ.get("TRENDING_SINCE", "daily").strip()
        or "daily"
    )

    def trending_url(self) -> str:
        url = TRENDING_BASE_URL
        if self.language:
            url += f"/{self.language}"
        return f"{url}?since={self.since}"


def _parse_count(text: str) -> int:
    """Parse a GitHub-formatted count like '12,345' or '324 stars today'."""
    digits = re.sub(r"[^\d]", "", text or "")
    return int(digits) if digits else 0


def _clean_text(text: str) -> str:
    """Collapse whitespace produced by joining text across inline tags."""
    return re.sub(r"\s+", " ", text or "").strip()


def fetch_html(url: str) -> str:
    """Fetch the raw HTML for a URL, raising on non-2xx responses."""
    response = requests.get(
        url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.text


def parse_trending(html: str) -> list[dict]:
    """Parse GitHub's trending page HTML into a list of repo dicts."""
    soup = BeautifulSoup(html, "lxml")
    items: list[dict] = []

    for rank, article in enumerate(soup.select("article.Box-row"), start=1):
        title_link = article.select_one("h2 a[href]")
        if not title_link or not title_link.get("href"):
            continue

        repo_path = title_link["href"].strip("/")
        if "/" not in repo_path:
            continue
        owner, name = repo_path.split("/", 1)

        description_tag = article.select_one("p.col-9")
        language_tag = article.select_one('[itemprop="programmingLanguage"]')
        stars_tag = article.select_one('a[href$="/stargazers"]')
        forks_tag = article.select_one('a[href$="/forks"]')
        period_tag = article.select_one("span.float-sm-right")

        items.append(
            {
                "rank": rank,
                "owner": owner,
                "name": name,
                "full_name": f"{owner}/{name}",
                "url": f"https://github.com/{repo_path}",
                "description": _clean_text(description_tag.get_text(" "))
                if description_tag
                else "",
                "language": language_tag.get_text(strip=True)
                if language_tag
                else None,
                "stars_total": _parse_count(stars_tag.get_text())
                if stars_tag
                else 0,
                "forks_total": _parse_count(forks_tag.get_text())
                if forks_tag
                else 0,
                "stars_in_period": _parse_count(period_tag.get_text())
                if period_tag
                else 0,
            }
        )

    return items


def scrape(config: Optional[Config] = None) -> dict:
    """Fetch and parse the GitHub trending page into a result dict."""
    config = config or Config()
    url = config.trending_url()
    html = fetch_html(url)
    items = parse_trending(html)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "source": url,
        "since": config.since,
        "language": config.language or None,
        "items": items,
    }


def save(data: dict, path: Path = OUTPUT_FILE) -> None:
    """Write scraped data to disk as JSON for the dashboard to consume."""
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    data = scrape()
    save(data)
    print(
        f"Scrape complete. Wrote {len(data.get('items', []))} item(s) "
        f"from {data.get('source')} to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
