from typing import List, Dict, Any
from .rules import RULES


def _raw_hits(text: str) -> List[Dict[str, Any]]:
    """Run all regex rules and collect raw hits (may overlap)."""
    hits: List[Dict[str, Any]] = []
    for rule in RULES:
        for m in rule.pattern.finditer(text):
            start, end = m.span()
            if start == end:
                continue
            hits.append(
                {
                    "start": start,
                    "end": end,
                    "label": rule.label,
                    "confidence": rule.confidence,
                    "rule": rule.name,
                    "priority": rule.priority,
                }
            )
    return hits


def _resolve_overlaps(spans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prefer higher-priority spans on overlap.
    If equal priority and same label, merge to the union; otherwise keep both but non-overlapping regions.
    (Simple first pass; we can refine with more nuanced merging later.)
    """
    if not spans:
        return []

    # Sort by (start asc, -priority desc, length desc)
    spans.sort(key=lambda s: (s["start"], -s["priority"], -(s["end"] - s["start"])))

    resolved: List[Dict[str, Any]] = []
    for span in spans:
        if not resolved:
            resolved.append(span)
            continue

        last = resolved[-1]
        if span["start"] >= last["end"]:
            # no overlap
            resolved.append(span)
            continue

        # overlap
        if span["priority"] > last["priority"]:
            # replace last with higher-priority current; but check if current also overlaps previous items.
            resolved[-1] = span
        elif span["priority"] == last["priority"] and span["label"] == last["label"]:
            # merge into union
            last["end"] = max(last["end"], span["end"])
        else:
            # keep the earlier (higher priority due to sort); drop/trim later span region that overlaps
            if span["end"] > last["end"]:
                # trim current to start at last end
                trimmed = span.copy()
                trimmed["start"] = last["end"]
                if trimmed["start"] < trimmed["end"]:
                    resolved.append(trimmed)
            # else fully covered → drop
    return resolved


def find_spans(text: str, strategy: str = "regex") -> List[Dict[str, Any]]:
    """
    Return list of spans: [{start, end, label, confidence, rule}]
    Strategy is a placeholder for future 'model' option.
    """
    if strategy != "regex":
        # For now we only support regex in this module.
        strategy = "regex"

    hits = _raw_hits(text)
    spans = _resolve_overlaps(hits)
    # Strip priority before returning
    for s in spans:
        s.pop("priority", None)
    return spans
