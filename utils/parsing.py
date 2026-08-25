"""Parsing helpers for the labeled intake response.

Kept out of the page script so the logic can be imported and tested without
starting Streamlit.
"""

import re

INTAKE_LABELS = [
    "PRIMARY_THERAPY",
    "SECONDARY_THERAPY",
    "EXPLANATION",
    "WHAT_IT_INVOLVES",
    "FIRST_APPOINTMENT",
    "CHECKLIST",
    "WELCOME_EMAIL",
]

# Tolerates the markdown the model sometimes adds around labels:
# "LABEL:", "**LABEL**:", "**LABEL:**", "### LABEL:".
_LABEL_PATTERN = re.compile(
    r"^\s*#{0,6}\s*(?:[*_]{1,2})?\s*("
    + "|".join(INTAKE_LABELS)
    + r")\s*(?:[*_]{1,2})?\s*:\s*(?:[*_]{1,2})?\s*"
)


def parse_sections(text):
    """Split a labeled response into {LABEL: body}. Missing labels are absent."""
    sections = {}
    current = None
    buffer = []
    for line in text.splitlines():
        match = _LABEL_PATTERN.match(line)
        if match:
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = match.group(1)
            buffer = [line[match.end():]]
        elif current:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer).strip()
    return sections


def bullets(text):
    """Cleaned bullet lines from a markdown-ish list."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^[-*•]\s*", "", line)
        if cleaned:
            out.append(cleaned)
    return out


def numbered_items(text):
    """Cleaned items from a numbered or bulleted list."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^(\d+[.)]|[-*•])\s*", "", line)
        if cleaned:
            out.append(cleaned)
    return out


def has_secondary(value):
    """True when SECONDARY_THERAPY names a real therapy rather than 'None'."""
    if not value:
        return False
    return value.strip().lower().rstrip(".") not in ("none", "n/a", "not applicable", "")
