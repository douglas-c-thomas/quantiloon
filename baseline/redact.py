from typing import List, Dict


def _token_label(label: str) -> str:
    return f"[[{label}]]"


def _apply_token_policy(text: str, spans: List[Dict]) -> str:
    """
    Replace each span with [[LABEL]] token.
    Assumes spans are non-overlapping and sorted.
    """
    if not spans:
        return text

    out = []
    i = 0
    for s in spans:
        start, end, label = s["start"], s["end"], s["label"]
        out.append(text[i:start])
        out.append(_token_label(label))
        i = end
    out.append(text[i:])
    return "".join(out)


def apply(text: str, spans: List[Dict], policy: str = "token") -> str:
    """
    Apply redactions to text using the chosen policy.
    Supported policies:
      - "token": replace with [[LABEL]]
      - (future) "mask": length-preserving masking with 'X'
      - (future) "drop": remove text
    """
    spans = sorted(spans, key=lambda s: s["start"])
    if policy == "token":
        return _apply_token_policy(text, spans)
    # Fallback to token for now
    return _apply_token_policy(text, spans)
