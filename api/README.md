# API Service

This folder implements the **FastAPI-based redaction service**. It exposes a simple REST interface for PHI detection and redaction, making the baseline (and future ML models) accessible via HTTP.

## Overview
The API wraps the baseline detection and redaction pipeline in a containerizable service. It provides two endpoints:

- **`GET /health`** → Returns service status and version.
- **`POST /redact`** → Accepts input text, applies the chosen redaction strategy, and returns structured spans plus redacted text.

## Request & Response Schema

### Request (`POST /redact`)
```json
{
  "text": "Dr. Jane Smith, MRN A12-9Z, seen 1/2/2024. Call 843-555-0199.",
  "strategy": "regex",
  "policy": "token"
}
```

- **text**: The input string to redact.
- **strategy**: Currently only `regex`; `model` will be added later.
- **policy**: Redaction method. Default: `token`.

### Response
```json
{
  "redacted_text": "[[PERSON]], MRN [[MRN]], seen [[DATE]]. Call [[PHONE]].",
  "spans": [
    {"start":0,"end":14,"label":"PERSON","confidence":0.86,"rule":"HONORIFIC_NAME"},
    {"start":16,"end":26,"label":"MRN","confidence":0.92,"rule":"MRN_TOKEN"},
    {"start":33,"end":41,"label":"DATE","confidence":0.95,"rule":"DATE_MDY"},
    {"start":48,"end":60,"label":"PHONE","confidence":0.98,"rule":"US_PHONE"}
  ],
  "meta": {"version":"0.1.0","strategy":"regex","policy":"token"}
}
```

- **redacted_text**: The input with PHI replaced by label tokens.
- **spans**: Structured PHI matches with offsets, labels, rules, and confidences.
- **meta**: Metadata about the API version and strategy.

## File Structure
```
api/
├── main.py       # FastAPI app with /health and /redact endpoints
└── schemas.py    # (optional) Pydantic models for request/response
```

## How to Run

### Local Development
```bash
uvicorn api.main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

### Example cURL
```bash
curl -s -X POST localhost:8000/redact \
  -H 'content-type: application/json' \
  -d '{"text":"Dr. Jane Smith, MRN A12-9Z, seen 1/2/2024. Call 843-555-0199."}'
```

### Docker Build & Run
```bash
docker build -t quantiloon-api:0.1.0 .
docker run -p 8000:8000 quantiloon-api:0.1.0
```

## Notes
- Designed for lightweight deployment and easy integration into Avandra’s Elixir/Phoenix pipeline.
- Schema-first design ensures response structure is predictable and machine-readable.
- Logging and version metadata included for traceability.

---
This API service is the integration layer for both baseline regex and upcoming ML-based redaction strategies.

