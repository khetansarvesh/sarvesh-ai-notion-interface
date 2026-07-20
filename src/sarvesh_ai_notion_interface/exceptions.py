"""Exceptions raised by :mod:`ai_skills_job_tracker`."""


class NotionJobTrackerError(Exception):
    """Base exception for this package."""


class NotionConfigurationError(NotionJobTrackerError):
    """Raised when required Notion configuration is missing."""


class NotionRequestError(NotionJobTrackerError):
    """Raised when a Notion API request cannot be completed."""
