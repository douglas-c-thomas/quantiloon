from baseline.detect import find_spans
from baseline.redact import apply

def test_basic_detection_and_redaction():
    text = "Patient John Doe, MRN Z99-123, on 01/02/2024. Phone 843-555-0199."
    spans = find_spans(text)
    labels = {s["label"] for s in spans}
    assert {"PERSON", "MRN", "DATE", "PHONE"} <= labels
    red = apply(text, spans)
    assert "[[PERSON]]" in red
    assert "[[MRN]]" in red
    assert "[[DATE]]" in red
    assert "[[PHONE]]" in red

