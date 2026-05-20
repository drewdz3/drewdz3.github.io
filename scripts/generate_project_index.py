import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER")
CURRENT_REPO = os.environ.get("GITHUB_REPOSITORY", "").split("/")[-1]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if not OWNER:
    print("GITHUB_REPOSITORY_OWNER is required.", file=sys.stderr)
    sys.exit(1)

if not GITHUB_TOKEN:
    print("GITHUB_TOKEN is required.", file=sys.stderr)
    sys.exit(1)


def get_json(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "docs-portal-generator",
        },
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def try_get_public_json(url: str):
    try:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "docs-portal-generator",
            },
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as ex:
        if ex.code == 404:
            return None
        raise
    except urllib.error.URLError:
        return None
    except json.JSONDecodeError:
        return None


def list_repos():
    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{OWNER}/repos?per_page=100&page={page}"
        page_repos = get_json(url)

        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    return repos


def render_project_index(sites):
    lines = [
        "# Project Documentation",
        "",
        "The following documentation sites are published from project repositories.",
        "",
    ]

    if not sites:
        lines.extend(
            [
                "No project documentation sites were discovered.",
                "",
            ]
        )
        return "\n".join(lines)

    grouped = {}

    for site in sites:
        site_type = site.get("type") or "project"
        grouped.setdefault(site_type, []).append(site)

    for site_type in sorted(grouped.keys()):
        heading = site_type.replace("-", " ").replace("_", " ").title()
        lines.append(f"## {heading}")
        lines.append("")

        for site in sorted(grouped[site_type], key=lambda item: item.get("name", "")):
            name = site.get("name") or site.get("slug") or "Unnamed documentation site"
            url = site.get("url")
            repo_url = site.get("repo_url")
            description = site.get("description") or ""

            if url:
                lines.append(f"### [{name}]({url})")
            else:
                lines.append(f"### {name}")

            if description:
                lines.append("")
                lines.append(description)

            if repo_url:
                lines.append("")
                lines.append(f"[Source repository]({repo_url})")

            lines.append("")

    return "\n".join(lines)


def main():
    repos = list_repos()
    sites = []

    for repo in repos:
        repo_name = repo.get("name")

        if not repo_name or repo_name == CURRENT_REPO:
            continue

        manifest_url = f"https://{OWNER}.github.io/{repo_name}/docs-site.json"
        manifest = try_get_public_json(manifest_url)

        if manifest:
            sites.append(manifest)

    output_path = Path("docs/projects/index.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_project_index(sites), encoding="utf-8")

    print(f"Discovered {len(sites)} documentation site(s).")
    for site in sites:
        print(f"- {site.get('name')} -> {site.get('url')}")


if __name__ == "__main__":
    main()