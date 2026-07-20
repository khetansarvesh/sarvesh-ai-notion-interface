"""Smoke tests for the installable package surface."""

import pytest

from sarvesh_ai_notion_interface import (
    __version__,
    company_matcher,
    config,
    db_applications,
    db_companies,
    db_connections,
    notion_client,
    page_preferences,
    page_reader,
)
from sarvesh_ai_notion_interface.exceptions import NotionConfigurationError


def test_package_version() -> None:
    assert __version__ == "0.1.0.dev1"


def test_public_modules_import_without_configuration() -> None:
    assert callable(notion_client.notion_request)
    assert callable(db_applications.add_scanned_job)
    assert callable(db_companies.add_company)
    assert callable(db_connections.add_connection)
    assert callable(company_matcher.match_company_name)
    assert callable(page_preferences.build_title_filter)
    assert callable(page_reader.fetch_page)


def test_project_name_normalization() -> None:
    assert config._normalize_title("Deep Research Agent") == "deep-research"


def test_missing_token_raises_exception_instead_of_exiting(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(notion_client, "NOTION_TOKEN", None)
    monkeypatch.setattr(page_reader, "NOTION_TOKEN", None)

    with pytest.raises(NotionConfigurationError):
        notion_client.notion_request("users/me", method="GET")
    with pytest.raises(NotionConfigurationError):
        page_reader.fetch_blocks("page-id")
