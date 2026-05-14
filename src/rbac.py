# RBAC: load policies and check access
import json
from pathlib import Path

_policies = json.loads((Path("data") / "access_policies.json").read_text())

USERS: dict = _policies["users"]
ROLES: dict = _policies["roles"]
DOC_TAGS: dict = _policies["document_tags"]

def authenticate(username: str, password: str) -> dict | None:
    user = USERS.get(username)
    if user and user["password"] == password:
        return user
    return None

def get_allowed_tags(role: str) -> list[str]:
    return ROLES.get(role, [])

def can_access(role: str, doc_source: str) -> bool:
    # return True if the role is allowed to see the given document source
    allowed = set(get_allowed_tags(role))
    doc_tags = set(DOC_TAGS.get(doc_source, []))
    return bool(allowed & doc_tags)
