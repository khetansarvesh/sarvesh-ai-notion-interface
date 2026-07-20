#!/usr/bin/env python3
"""
Shared Notion API client.

Provides authenticated HTTP requests and paginated database queries.
Used by all other notion modules.

Usage (CLI):
  python3 scripts/notion/notion_client.py --test
"""

import json
import logging
import sys
import time

import requests

from .config import NOTION_API, NOTION_TOKEN
from .exceptions import NotionConfigurationError, NotionRequestError

logger = logging.getLogger(__name__)


def notion_request(
    endpoint: str,
    method: str = "POST",
    data: dict | None = None,
    timeout: int = 30,
    max_retries: int = 5,
) -> dict:
    """Make an authenticated request to the Notion API.

    Args:
        endpoint: API path (e.g., "databases/{id}/query" or "pages/{id}")
        method: HTTP method (GET, POST, PATCH)
        data: Dict to send as JSON body (optional)

    Returns:
        Parsed JSON response dict.
    """
    if not NOTION_TOKEN:
        raise NotionConfigurationError("NOTION_TOKEN environment variable not set.")

    url = f"{NOTION_API}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    payload = json.dumps(data).encode() if data else None

    attempt = 0
    while True:
        try:
            resp = requests.request(method, url, headers=headers, data=payload, timeout=timeout)
            if resp.status_code in {429, 500, 502, 503, 504} and attempt < max_retries:
                retry_after = resp.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else min(2**attempt, 30)
                logger.warning(
                    f"Retrying Notion request after HTTP {resp.status_code} in {delay:.1f}s: {endpoint}",
                )
                time.sleep(delay)
                attempt += 1
                continue
            if not resp.ok:
                raise NotionRequestError(
                    f"HTTP {resp.status_code} from {endpoint}: {resp.text[:200]}"
                )
            return resp.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt < max_retries:
                delay = min(2**attempt, 30)
                logger.warning(
                    f"Retrying Notion request after network error in {delay:.1f}s: {endpoint} ({e})",
                )
                time.sleep(delay)
                attempt += 1
                continue
            raise NotionRequestError(f"Network error while requesting {endpoint}: {e}") from e


def notion_post(path: str, body: dict | None = None) -> dict:
    """Convenience alias for notion_request with POST method."""
    return notion_request(path, method="POST", data=body)


def load_all_rows(db_id: str, filter_body: dict | None = None) -> list[dict]:
    """Load all rows from a Notion database, handling pagination.

    Args:
        db_id: Notion database ID
        filter_body: Optional filter dict for the query

    Returns:
        List of row dicts (Notion page objects).
    """
    rows = []
    cursor = None

    while True:
        body = {"page_size": 100}
        if filter_body:
            body["filter"] = filter_body
        if cursor:
            body["start_cursor"] = cursor

        data = notion_post(f"databases/{db_id}/query", body)
        rows.extend(data.get("results", []))

        if data.get("has_more"):
            cursor = data.get("next_cursor")
        else:
            break

    return rows


def main() -> None:
    if "--test" in sys.argv:
        try:
            result = notion_request("users/me", method="GET")
            print(f"OK: Connected as {result.get('name', 'unknown')}")
        except (NotionConfigurationError, NotionRequestError) as error:
            print(f"FAIL: {error}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python3 scripts/notion/notion_client.py --test")


if __name__ == "__main__":
    main()
