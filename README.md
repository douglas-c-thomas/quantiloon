# Quantiloon

Pre‑kickoff scaffolding for a de‑identification (de‑id) redaction service. This repo contains a **regex baseline** for PHI detection and a **FastAPI** service exposing `/redact`.

> ⚠️ **No real PHI**: Only synthetic or public/approved text is used during ramp‑up.

---

## Contents
- [`/baseline`](./baseline) — Regex rules, span detection, redaction policies, synthetic generator, evaluation harness
- [`/api`](./api) — FastAPI service with `/health` and `/redact`
- [`/data`](./data) — Synthetic samples (generated locally)
- [`/tests`](./tests) — Unit tests for baseline behavior

---

## Quickstart

### 1) Python & env
```bash
# ensure pyenv is initialized in your shell
# ~/.zshrc:
# export PYENV_ROOT="$HOME/.pyenv"
# [[ -d "$PYENV_ROOT/bin" ]] && export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"

pyenv install 3.11.9 -s
pyenv local 3.11.9
python --version   # -> Python 3.11.9

python -m venv .venv
source .venv/bin/activate
pip install -U pip
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run the API
```bash
uvicorn api.main:app --reload
# open http://127.0.0.1:8000/docs
```

### 4) Try it
```bash
curl -s -X POST localhost:8000/redact \
  -H 'content-type: application/json' \
  -d '{"text":"Dr. Jane Smith, MRN A12-9Z, seen 1/2/2024. Call 843-555-0199."}'
```

---

## Baseline, Spans, and Resolution (high level)
- **Span**: `{start, end, label, confidence, rule}` where `start/end` are character offsets within the input.
- **Rules**: Regex patterns produce candidate spans with a label (e.g., PERSON, DATE, MRN) and static confidence priors.
- **Resolution**: Candidates are sorted by `start` and priority; on overlap, higher‑priority spans win; identical label+priority can merge; output is non‑overlapping, ordered spans.
- **Redaction policy**: Replace each span with `[[LABEL]]` tokens (`token` policy). Other policies (mask, drop) can be added.

See [`/baseline/README.md`](./baseline/README.md) for details and a diagram.

---

## Developer Guide

### Generate synthetic data
```bash
python -m baseline.synth_gen --n 100 --out data/synth.jsonl
```

### Evaluate baseline (bootstrap mode)
```bash
python -m baseline.evaluate --data data/synth.jsonl --out out/report.json
```

### Run unit tests
```bash
python -m pytest -q
```

### Project structure
```
quantiloon/
├─ api/               # FastAPI app
├─ baseline/          # regex baseline + eval harness
├─ data/              # synthetic samples (git‑ignored if large)
├─ docs/              # design notes, ADRs, etc.
├─ tests/             # unit tests
├─ requirements.txt
├─ pyproject.toml     # version pins and tooling
└─ README.md          # this file
```

---

## Operating Rules (working draft)
- **Bias to execution**: Minimal, runnable artifacts in each commit.
- **Clarity > cleverness**: Document assumptions and trade‑offs.
- **Reproducibility**: Version‑pin dependencies; deterministic runs.
- **Compliance**: No real PHI in this repo; synthetic/public only.
- **Metrics first**: Define how we measure improvements before changing models/rules.

---

## Next Steps (roadmap excerpt)
- Gold‑label synthetic generator (emit exact spans alongside text)
- Evaluation harness against gold spans (per‑label P/R/F1)
- Model shortlist runner (Hugging Face NER baselines) vs regex
- Elixir/Phoenix client stub calling the `/redact` endpoint
- Dockerfile + compose for local env parity

---

## License
TBD (placeholder).
# quantiloon
Quantiloon
