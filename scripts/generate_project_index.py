import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER")
CURRENT_REPO = os.environ.get("GITHUB_REPOSITORY", "").split("/")[-1]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

PROJECTS_DIR = Path("docs/projects")


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


def safe_file_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "documentation-site"


def clean_generated_project_pages():
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    for path in PROJECTS_DIR.glob("*.md"):
        if path.name != "index.md":
            path.unlink()


def render_projects_index(sites):
    lines = [
        "# Projects",
        "",
        "The following project documentation sites are available.",
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

    for site in sorted(sites, key=lambda item: item.get("name", "")):
        name = site.get("name") or site.get("slug") or "Unnamed documentation site"
        url = site.get("url")
        description = site.get("description") or ""

        if url:
            lines.append(f"- [{name}]({url})")
        else:
            lines.append(f"- {name}")

        if description:
            lines.append(f"  - {description}")

    lines.append("")
    return "\n".join(lines)


def render_project_page(site):
    name = site.get("name") or site.get("slug") or "Unnamed documentation site"
    url = site.get("url")
    repo_url = site.get("repo_url")
    description = site.get("description") or ""

    lines = [
        f"# {name}",
        "",
    ]

    if description:
        lines.extend(
            [
                description,
                "",
            ]
        )

    if url:
        lines.extend(
            [
                f"[Open documentation site]({url})",
                "",
            ]
        )

    if repo_url:
        lines.extend(
            [
                f"[Source repository]({repo_url})",
                "",
            ]
        )

    return "\n".join(lines)


def render_projects_pages_file(sites):
    lines = [
        "nav:",
        "  - Overview: index.md",
    ]

    for site in sorted(sites, key=lambda item: item.get("name", "")):
        name = site.get("name") or site.get("slug") or "Unnamed documentation site"
        file_name = site["_generated_file_name"]
        safe_name = name.replace('"', '\\"')
        lines.append(f'  - "{safe_name}": {file_name}')

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
            slug = manifest.get("slug") or repo_name
            manifest["_generated_file_name"] = f"{safe_file_name(slug)}.md"
            sites.append(manifest)

    clean_generated_project_pages()

    (PROJECTS_DIR / "index.md").write_text(
        render_projects_index(sites),
        encoding="utf-8",
    )

    for site in sites:
        project_page_path = PROJECTS_DIR / site["_generated_file_name"]
        project_page_path.write_text(
            render_project_page(site),
            encoding="utf-8",
        )

    (PROJECTS_DIR / ".pages").write_text(
        render_projects_pages_file(sites),
        encoding="utf-8",
    )

    print(f"Discovered {len(sites)} documentation site(s).")
    for site in sites:
        print(f"- {site.get('name')} -> {site.get('url')}")


if __name__ == "__main__":
    main()