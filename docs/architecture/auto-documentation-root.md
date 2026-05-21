# Documentation Root Setup

## Summary

To setup a documentation root site that dynamically links to all other documentation sites within the organization, follow this guide.

---

## Change History

| Date | Purpose of Change | Contributors |
|---|---|---|
| 2026-05-21 | Initial draft | Andrew D'Alton |

---

## Status

| Status | Decision Owner | Reviewers | Last Reviewed | Next Review |
| --- | --- | --- | --- | --- |
| **Proposed** | Architecture Team | Architecture Team | 2026-05-21 | not applicable |

---

## Context

Traditionally here at Aya, we have placed all forms of documentation into Confluence. This has worked well enough, but many have reported frustration that documentation is hard to find, and its even harder to determine which documentation is really current from that which is just an opinion. We have created a method whereby project documentation can be automatically exported to HTML and published to GitHub pages, and made discoverable from our central hub by following a few simple steps.

---

## Goals

The purpose of this document is to provide guidance on setting up the central documentation hub of this feature.

---

## Setup

In Aya Healthcare, this should already be set up. If you would like to set this up for another organization you can use the Aya implementation as reference. Copy files as listed with minor changes as needed.

> NOTE: Whenever a new "child" repository is created/enabled, the root site must be regenerated so that the "child" site can be discovered and included in the nav.

Child repositories are only discovered during the build process and not through some other mechanism while the site is published - all these sites are static web sites.

### Create a documentation root repository

Typically, the architecture organization owns technical documentation, and so the root documentation repository would house any over-arching or cross-cutting architectural documents that aren't linked to any specific project or repository. Examples are:
- ADRs that affect the entire organization
- Architectural standards and best practices
- Outcomes from investigations or POCs that can be useful for teams when a specific technology is required.

In GitHub, create a new repository with the following name:

> `[org_name].github.io` eg: `AyaHealthcare.github.io`

This special naming that is reserved for this purpose.

During creating allow GitHub to create an initial `readme.md` file.

### Setup GitHub pages

- In your `[org_name].github.io` repository
- Open Settings
- Select Pages
- Under `Build and deployment` Set `Source` to `GitHub Actions`
- The site url will be `https://[org_name].github.io`, eg: `https://AyaHealthcare.github.io`
  
You must either have a paid subscription with pages enabled, or your repository must be public to do this.

### Create your documentation folder

In your repository, create a new folder

> `docs`

Copy the following files into your `docs` folder:
- `.pages`
- `index.md`
- `logo.svg`
- `styles.css`

### Create the `.pages` file

Inside your docs folder, create a new file named `.pages` with the following content:

> ``nav:
> ``  - architecture
> ``  - projects
> ``  - index.md
> ``  - "... | regex=^(?!index\\.md$).*"

Note that the content of this file is different from the same file in "child" repositories. Here we explicitly create nav sections for the content we want to publish. All discovered repositories will be listed under `projects`. You can add any other groups you want here.

### Copy `mkdocs.yml`

In the root of your repository, copy `mkdocs.yml`. This tells the GitHub action how to process your files. No changes are needed to this file when copied from an existing documentation root repository.

### Create the scripts folder

- Create a new folder called `scripts` in the root of your project. 
- `scripts` and `docs` must be siblings. 
- Copy `generate_project_index.py` into `scripts`

This script iterates repositories in the organization and lists those with the doc discovery JSON file, `docs-site.json`. It then reads the content of the file to get a description of the site and places a link in the nav. The project link will link to the "child" repositories `docs/index.html` page. This page is auto-generated from the project's default `readme.md`.

### Create the workflow

- In the root of your repository, create the folder structure `.github/workflows` if it doesn't already exit.
- Copy the file `pages.yml` into `.github/workflows`

No changes are needed for this to work.

## Explanation

`.github/workflows/pages.yml` is executed whenever changes are pushed into your main branch. During execution, `pages.yml` does the following:
- Sets up everything `mkdocs` needs to convert your markdown files to HTML
- Creates the variables that will be used in the process:
...- `REPO_FULL_NAME`
...- `REPO_NAME`
...- `REPO_URL`
...- `PAGES_URL`
...-`SITE_NAME` - Derived title for your pages site.
- Execute the python script `generate_project_index.py` to discover child repositories and dynamically create nav items for them.
- Executes `mkdocs.yml` to convert "local" markdown to HTML
...- Sets up navigation
...- Creates a light/dark mode switch
...- Enables search
...- Creates a link to the repository
- Publishes the pages site.

## Summary

In this document we have:
- Setup the special case repository to enable GitHub pages as a documentation root.
- Created or copied the needed files to support the process
...- `mkdocs.yml`
...- `docs/.pages`
...- `docs/index.md`
...- `docs/logo.svg`
...- `docs/styles.css`
...- `scripts/generate_project_index.py`
...- `.github/workflows/pages.yml`

Now that you have a documentation root setup, check out our guide for setting up individual "child" repositories that can be discovered and dynamically included in this structure.
