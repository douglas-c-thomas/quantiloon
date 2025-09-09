from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any
from baseline.detect import find_spans
from baseline.redact import apply as apply_redactions

app = FastAPI(title="Quantiloon Redactor", version="0.1.0")

class RedactRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    strategy: Literal["regex", "model"] = "regex"
    policy: Literal["token"] = "token"  # extend later

class Span(BaseModel):
    start: int
    end: int
    label: str
    confidence: float
    rule: str

class RedactResponse(BaseModel):
    redacted_text: str
    spans: List[Span]
    meta: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/redact", response_model=RedactResponse)
def redact(req: RedactRequest):
    spans = find_spans(req.text, strategy=req.strategy)
    red_text = apply_redactions(req.text, spans, policy=req.policy)
    return {
        "redacted_text": red_text,
        "spans": spans,
        "meta": {"version": "0.1.0", "strategy": req.strategy, "policy": req.policy},
    }

