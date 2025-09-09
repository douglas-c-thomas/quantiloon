import re
from dataclasses import dataclass
from typing import Pattern, List


@dataclass(frozen=True)
class Rule:
    label: str
    name: str
    pattern: Pattern
    confidence: float
    priority: int  # higher wins on overlap


def _compile(pattern: str, flags: int = 0) -> Pattern:
    return re.compile(pattern, flags)


# Priority guidance:
# Highly specific identifiers > contact info > dates/ids > person/address-ish > misc
# (higher integer = higher priority)
RULES: List[Rule] = [
    # Emails & URLs
    Rule(
        label="EMAIL",
        name="EMAIL_SIMPLE",
        pattern=_compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[A-Za-z]{2,}\b"),
        confidence=0.99,
        priority=90,
    ),
    Rule(
        label="URL",
        name="URL_HTTP",
        pattern=_compile(r"\bhttps?://\S+\b"),
        confidence=0.98,
        priority=80,
    ),

    # Phones
    Rule(
        label="PHONE",
        name="US_PHONE",
        pattern=_compile(r"(?:\+1[\s\-.])?\(?\d{3}\)?[\s\-.]\d{3}[\s\-.]\d{4}\b"),
        confidence=0.98,
        priority=85,
    ),

    # MRN / IDs (very rough first pass; tune later)
    Rule(
        label="MRN",
        name="MRN_TOKEN",
        pattern=_compile(r"(?i)\b(?:MRN|MedRec|Patient(?:\s*ID)?)\W*[A-Z0-9\-]{4,}\b"),
        confidence=0.92,
        priority=88,
    ),

    # Dates (common formats; we’ll iterate later)
    Rule(
        label="DATE",
        name="DATE_MDY",
        pattern=_compile(r"\b(?:0?[1-9]|1[0-2])[\/\-](?:0?[1-9]|[12]\d|3[01])[\/\-](?:\d{2}|\d{4})\b"),
        confidence=0.95,
        priority=75,
    ),
    Rule(
        label="DATE_YMD",
        name="DATE_YMD",
        pattern=_compile(r"\b\d{4}[\/\-](?:0?[1-9]|1[0-2])[\/\-](?:0?[1-9]|[12]\d|3[01])\b"),
        confidence=0.95,
        priority=75,
    ),
    Rule(
        label="DATE",
        name="DATE_LONG",
        pattern=_compile(
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? "
            r"(?:0?[1-9]|[12]\d|3[01]),? \d{4}\b",
            re.IGNORECASE,
        ),
        confidence=0.94,
        priority=74,
    ),

    # Addresses (very rough heuristic; iterate later)
    Rule(
        label="ADDRESS",
        name="ADDRESS_STREET",
        pattern=_compile(
            r"\b\d{1,6}\s+\w+(?:\s\w+){0,3}\s(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Way|Ct|Court)\b",
            re.IGNORECASE,
        ),
        confidence=0.80,
        priority=60,
    ),
    Rule(
        label="ZIP",
        name="US_ZIP",
        pattern=_compile(r"\b\d{5}(?:-\d{4})?\b"),
        confidence=0.90,
        priority=70,
    ),

    # Person-ish (very naive first pass)
    Rule(
        label="PERSON",
        name="HONORIFIC_NAME",
        pattern=_compile(r"\b(?:Dr|Mr|Mrs|Ms)\.?\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b"),
        confidence=0.86,
        priority=65,
    ),
    Rule(
        label="PERSON",
        name="CAP_NAME",
        pattern=_compile(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b"),
        confidence=0.83,
        priority=55,
    ),

    # Age (policy TBD; often redacting <89 is required—configurable later)
    Rule(
        label="AGE",
        name="AGE_SIMPLE",
        pattern=_compile(r"\b(?:age|aged)\s*(\d{1,3})\b", re.IGNORECASE),
        confidence=0.80,
        priority=50,
    ),
]
