# sarvesh-ai-notion-interface

Reusable Python helpers for Notion-backed AI job-tracking workflows.

This package provides:

- authenticated, retried Notion API requests;
- database pagination;
- job-application, company, and connection database helpers;
- company-name matching;
- fetching Notion pages and preferences.

It is intentionally **not** a general-purpose Notion SDK. Its database helpers
expect the schemas documented by the consuming job skills.

## Install

Until the first PyPI release, install from a local checkout:

```bash
python -m pip install -e .
```

After publishing:

```bash
python -m pip install sarvesh-ai-notion-interface
```

## Configuration

Set configuration through environment variables:

```bash
export NOTION_TOKEN="secret_..."
export NOTION_DB_APPLICATIONS="..."
export NOTION_DB_COMPANIES="..."
export NOTION_DB_CONNECTIONS="..."
export NOTION_PAGE_PARENT="..."
```

For local development, put the same variables in a `.env` file in the current
directory, or set `AI_SKILLS_ENV_FILE` to the absolute path of a `.env` file.
Environment variables always take precedence.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
python -m build
```

## Publishing checklist

Before creating a public GitHub repository or publishing to PyPI:

1. Create the GitHub repository and update the URLs in `pyproject.toml`.
2. Create a TestPyPI release, install it in a clean virtual environment, and
   run the consuming skills against it.
3. Publish the validated version to PyPI.

No secrets, database IDs, resumes, or personal candidate data belong in this
repository.
