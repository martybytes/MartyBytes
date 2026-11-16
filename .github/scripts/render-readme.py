"""Render the profile README's activity sections from small GitHub queries.

README.gtpl holds comment markers, each replaced literally in one pass, so
repository descriptions and pull-request titles are never executed as template
code. Adapted from ChrisTitusTech/ChrisTitusTech, with additions: a curated
project list (featured.json) with live star counts, a one-line "Now", no repeats
between "Currently working on" and "Latest projects", no dangling dash after an
empty description, and Markdown metacharacters in GitHub-supplied text escaped.
"""

import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import urlencode


PER_SECTION = 3
STARS_SHOWN_FROM = 10
FEATURED = Path(__file__).resolve().parents[2] / "featured.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      commitContributionsByRepository(maxRepositories: 100) {
        repository { nameWithOwner url description isPrivate }
        contributions(last: 1) { nodes { occurredAt } }
      }
    }
  }
}
"""

MARKER = re.compile(r"\{\{ /\* ([A-Z_]+) \*/ \}\}")

# Blocks another workflow owns (waka.yml writes the WakaTime stats); a re-render
# keeps whatever is between these markers in the current README.
KEPT_SECTIONS = ("waka",)


def api(arguments):
    for attempt in range(3):
        try:
            result = subprocess.run(
                ["gh", "api", *arguments],
                check=True, capture_output=True, text=True, timeout=60,
            )
            data = json.loads(result.stdout)
            if isinstance(data, dict) and data.get("errors"):
                raise ValueError("GitHub returned GraphQL errors")
            return data
        except (subprocess.SubprocessError, ValueError, KeyError, TypeError):
            if attempt == 2:
                raise RuntimeError("GitHub query failed after 3 attempts") from None
            print("GitHub query failed; retrying", file=sys.stderr)
            time.sleep(5 * (attempt + 1))


def clean(value):
    """Collapse to one line and escape what would break a Markdown link or table."""
    text = " ".join((value or "").split())
    return re.sub(r"([\\\[\]|<>*_`])", r"\\\1", text)


def repo_line(name, url, description):
    description = clean(description)
    return f"- [{name}]({url})" + (f" — {description}" if description else "")


def stars_label(count):
    """'' below the threshold (0 stars is worse than saying nothing), else '999 stars' or '1.2k+ stars'."""
    if count < STARS_SHOWN_FROM:
        return ""
    if count < 1000:
        return f"{count} stars"
    thousands = math.floor(count / 100) / 10
    return f"{thousands:g}k+ stars"


def featured_lines(featured, repos):
    lines = []
    for item in featured:
        repo = repos.get(item["repo"])
        if not repo or repo["isPrivate"] or repo["isFork"]:
            print(f"Skipping featured {item['repo']}: missing, private or a fork", file=sys.stderr)
            continue
        name = item["repo"].split("/", 1)[1]
        stars = stars_label(repo["stargazerCount"])
        lines.append(f"- **[{name}]({repo['url']})** — {item['blurb']}"
                     + (f" ({stars})" if stars else ""))
    return lines


def featured_query(featured):
    parts = []
    for i, item in enumerate(featured):
        owner, name = item["repo"].split("/", 1)
        parts.append(f'r{i}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) '
                     "{ nameWithOwner url stargazerCount isPrivate isFork }")
    return "query {\n  " + "\n  ".join(parts) + "\n}"


def now_line(pull, repo):
    """The newer of the latest public pull request and the latest new repository."""
    if pull and (not repo or pull["created_at"] >= repo["created_at"]):
        name = pull["repository_url"].split("/repos/", 1)[1]
        return (f'**Now:** [{clean(pull["title"])}]({pull["html_url"]}) '
                f"in [{name}](https://github.com/{name})")
    if repo:
        description = clean(repo["description"])
        return (f'**Now:** started [{repo["full_name"]}]({repo["html_url"]})'
                + (f" — {description}" if description else ""))
    return "**Now:** nothing public this week."


def is_self(name, login):
    return name.lower() == f"{login}/{login}".lower()


def recent_contributions(entries, login):
    entries = [entry for entry in entries
               if not entry["repository"]["isPrivate"]
               and not is_self(entry["repository"]["nameWithOwner"], login)
               and entry["contributions"]["nodes"]]
    entries.sort(key=lambda entry: entry["contributions"]["nodes"][0]["occurredAt"],
                 reverse=True)
    return [entry["repository"] for entry in entries[:PER_SECTION]]


def latest_repos(repos, login, exclude):
    exclude = {name.lower() for name in exclude}
    picked = [repo for repo in repos
              if not repo["fork"] and not repo["private"]
              and not is_self(repo["full_name"], login)
              and repo["full_name"].lower() not in exclude]
    return picked[:PER_SECTION]


def pr_line(pr):
    repo = pr["repository_url"].split("/repos/", 1)[1]
    return f'- [{clean(pr["title"])}]({pr["html_url"]}) on [{repo}](https://github.com/{repo})'


def render(template, sections):
    for name in sections:
        if template.count("{{ /* " + name + " */ }}") != 1:
            raise ValueError(f"Expected exactly one {name} marker")
    # One pass prevents substituted repository text from being interpreted again.
    return MARKER.sub(lambda match: "\n".join(sections[match[1]] or ["- Nothing yet."]),
                      template)


def keep_sections(rendered, previous):
    for name in KEPT_SECTIONS:
        start, end = f"<!--START_SECTION:{name}-->", f"<!--END_SECTION:{name}-->"
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        old = pattern.search(previous)
        if old and pattern.search(rendered):
            rendered = pattern.sub(lambda _: old[0], rendered, count=1)
    return rendered


def sections(login):
    featured = json.loads(FEATURED.read_text())
    stars = api(["graphql", "-f", f"query={featured_query(featured)}"])["data"]
    result = {"FEATURED": featured_lines(
        featured, {r["nameWithOwner"]: r for r in stars.values() if r})}

    data = api(["graphql", "-f", f"query={QUERY}", "-f", f"login={login}"])
    entries = data["data"]["user"]["contributionsCollection"]["commitContributionsByRepository"]
    working = recent_contributions(entries, login)
    result["RECENT_CONTRIBUTIONS"] = [repo_line(r["nameWithOwner"], r["url"], r["description"])
                                       for r in working]

    shown = [r["nameWithOwner"] for r in working]
    repos, page = [], 1
    while len(latest_repos(repos, login, shown)) < PER_SECTION:
        batch = api([f"users/{login}/repos?sort=created&direction=desc&per_page=100&page={page}"])
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    result["RECENT_REPOS"] = [repo_line(r["full_name"], r["html_url"], r["description"])
                              for r in latest_repos(repos, login, shown)]

    query = urlencode({"q": f"type:pr author:{login} is:public -repo:{login}/{login}",
                       "sort": "created", "order": "desc", "per_page": PER_SECTION})
    pulls = api([f"search/issues?{query}"])
    if pulls.get("incomplete_results"):
        raise RuntimeError("GitHub returned incomplete pull-request results")
    result["RECENT_PULL_REQUESTS"] = [pr_line(pr) for pr in pulls["items"]]

    newest = next((r for r in repos if not r["fork"] and not r["private"]
                   and not is_self(r["full_name"], login)), None)
    result["NOW"] = [now_line(pulls["items"][0] if pulls["items"] else None, newest)]

    stars = api([f"users/{login}/starred?sort=created&direction=desc&per_page={PER_SECTION}"])
    result["RECENT_STARS"] = [repo_line(r["full_name"], r["html_url"], r["description"])
                              for r in stars if not r["private"]]
    return result


if __name__ == "__main__":
    login = os.environ["GITHUB_REPOSITORY_OWNER"]
    template = Path(sys.argv[1]).read_text()
    target = Path(sys.argv[2])
    previous = target.read_text() if target.exists() else ""
    target.write_text(keep_sections(render(template, sections(login)), previous))
