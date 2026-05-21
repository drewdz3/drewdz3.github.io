# Enabling Auto-Documentation

## Summary

To have your repository or a new repository automatically be included in this site and browseable within the company, follow these simple steps.

---

## Change History

| Date | Purpose of Change | Contributors |
|---|---|---|
| 2026-05-20 | Initial draft | Andrew D'Alton |

---

## Status

**Status:** Proposed

**Decision Owner:**  
Architecture Team

**Reviewers:**  
Architecture Team

**Last Reviewed:**  
2026-05-21

**Next Review:**  
not applicable.

---

## Context

Traditionally here at Aya, we have placed all forms of documentation into Confluence. This has worked well enough, but many have reported frustration that documentation is hard to find, and its even harder to determine which documentation is really current from that which is just an opinion. We have create a method whereby project documentation can be automatically exported to HTML and published to GitHub pages, and made discoverable from our central hub by following a few simple steps.

---

## Goals

The purpose of this document is to provide guidance on setting up this feature.

---

## Setup

The folder structure and files referenced in this guide can be copied from this or (almost) any existing repository that uses this pattern.

### Setup GitHub pages

- Inside your repository on GitHub
- Open Settings
- Select Pages
- Under `Build and deployment` Set `Source` to `GitHub Actions`
- Once a build has been complete return here to find your site URL above `Build and deployment`
  
You must either have a paid subscription with pages enabled, or your repository must be public to do this.

### Create your documentation folder

In your repository, create a new folder

> `docs`

Copy the following files into your `docs` folder:
- `logo.svg`
- `styles.css`

### Create the `.pages` file

Inside your docs folder, create a new file named `.pages` with the following content:

> ``nav:
> ``  - index.md
> ``  - ...

This file tells `mkdocs`, our GitHub action, how to order your files. In this case, index first, then everything else. You can add files here if you want them in a specific order.

### Create the discovery contract

Also in `docs`, create a new file, `docs-site.json` with the following content:

> `` {
> ``   "name": "[human readable name / title]",
> ``   "slug": "[repo_name]",
> ``   "repo": "[repo_relative_path]",
> ``   "repo_url": "[repo_full_path]",
> ``   "url": "[repo_pages_full_path]",
> ``   "description": "[Some description of your project]",
> ``   "type": "project"
> `` }

This file is the contract that allows your repository to be discovered by the root and describes it.

### Copy `mkdocs.yml`

In the root of your repository, copy `mkdocs.yml`. This tells the GitHub action how to process your files. No changes are needed to this file.

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
- Executes `mkdocs.yml` to convert markdown to HTML
...- Sets up navigation
...- Creates a light/dark mode switch
...- Enables search
...- Links back to the documentation root page
...- Creates a link to the repository
- Uploads the converted HTML to the pages site.

## Summary

In this document we have:
- Setup the repository to enable GitHub pages
- Created or copied the needed files to support the process
...- `mkdocs.yml`
...- `docs/index.md`
...- `docs/docs-site.json`
...- `docs/logo.svg`
...- `docs/styles.css`
...- `.github/workflows/pages.yml`

If you're interested check out the guide for setting up the documentation root that also discovers all other sites.
