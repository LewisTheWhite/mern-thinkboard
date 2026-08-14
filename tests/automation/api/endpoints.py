"""
API endpoint definitions and helpers.
"""

from dataclasses import dataclass


@dataclass
class AuthEndpoints:
    """Authentication endpoint constants."""
    SIGNUP = "auth/signup"
    LOGIN = "auth/login"
    ME = "auth/me"


@dataclass
class NotesEndpoints:
    """Notes endpoint constants."""
    LIST = "notes"
    CREATE = "notes"

    def GET(self, note_id):
        return f"notes/{note_id}"

    def UPDATE(self, note_id):
        return f"notes/{note_id}"

    def DELETE(self, note_id):
        return f"notes/{note_id}"


@dataclass
class LabelsEndpoints:
    """Label endpoint constants."""
    LIST = "labels"
    CREATE = "labels"

    def DELETE(self, label_id):
        return f"labels/{label_id}"


# Export for easy import
AUTH = AuthEndpoints()
NOTES = NotesEndpoints()
LABELS = LabelsEndpoints()
