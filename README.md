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

The PyPI publisher uses GitHub's OpenID Connect identity rather than a stored
API token. Before the first release:

1. In PyPI, create a **Trusted Publisher** with:
   - PyPI project name: `sarvesh-ai-notion-interface`
   - Owner: `khetansarvesh`
   - Repository: `sarvesh-ai-notion-interface`
   - Workflow filename: `publish-pypi.yml`
   - Environment name: `pypi`
2. Push tag `v0.1.0`, or run the **Publish to PyPI** workflow
   manually from GitHub Actions.
3. Install the result in a clean virtual environment:

   ```bash
   python -m pip install sarvesh-ai-notion-interface==0.1.0
   ```

4. Run the consuming skills against that clean installation.

No secrets, database IDs, resumes, or personal candidate data belong in this
repository.
