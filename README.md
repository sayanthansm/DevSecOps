Set-Content -Path 'd:\CODE\Projects\DevSecOps\README.md' -Value @'
# DevSecOps: Policy-Driven Secret Leak Prevention in CI/CD

## Overview

Modern software teams frequently leak secrets (API keys, tokens, credentials) into source code repositories. While CI/CD platforms can report failures, they do not define or enforce security policy.

This project implements a custom, explainable, policy-as-code security gate that detects hardcoded secrets early ("shift-left"), enforces configurable security rules, and guides developers toward secure remediation — all integrated into CI/CD.

## Problem Statement

**Developers accidentally commit secrets into repositories.**

Existing detection mechanisms often:
- Trigger too late
- Lack enforcement
- Provide poor remediation guidance
- Are tightly coupled to specific CI platforms

**Goal:** Build a tool-agnostic, policy-driven CI/CD security gate that:
- Detects secrets early
- Enforces risk-based policies
- Provides actionable fixes
- Measures security posture over time

## Key Features

### Shift-Left Secret Detection
- Scans source code before deployment
- Works locally and in CI/CD
- Supports `.py`, `.js`, `.env`, `.csv`

### Risk-Based Severity Classification
Secrets are classified into:
- **HIGH** – Critical secrets (e.g., AWS Access Keys)
- **MEDIUM** – Generic API keys & tokens
- **INVALID** – Non-secret strings (ignored)

### Policy-as-Code Enforcement
Security behavior is not hardcoded. Defined via `scanner/policy.yml`:

```yaml
enforcement:
  block:
    - HIGH
  warn:
    - MEDIUM
```

This allows:
- Flexible enforcement
- Environment-specific policies
- Behavior changes without code changes

### Explainable Security Output
Each finding includes:
- Secret type
- Severity
- File & line number
- Clear remediation steps

**Example:**
```
❌ AWS Access Key (HIGH)
Location: demo-app/test_keys.csv:2
Fix:
  - Remove hardcoded key
  - Store in GitHub Secrets
  - Access via environment variables
```

### Developer-Friendly (DX-Focused)
- PR-friendly output formatting
- Clear fix suggestions
- No cryptic security messages

### Controlled Evaluation via CSV Dataset
- Curated dataset with high-risk and medium-risk secrets
- Invalid (negative) test cases
- Ensures reproducible testing
- Avoids randomness & false negatives

### Metrics & Accuracy Reporting
Provides:
- Number of files scanned
- Severity counts
- Detection accuracy
- Ignored entries

### Security Regression Detection
Tracks security posture across runs:
```
⚠ HIGH increased: 2 → 4
⚠ MEDIUM increased: 2 → 4
```

Helps teams detect worsening security trends, not just single failures.

## Architecture Overview

```
Commit / Push
    ↓
CI Pipeline (GitHub Actions)
    ↓
Custom Secret Scanner
    ↓
Policy-as-Code Evaluation
    ↓
Pass / Block Decision
    ↓
Developer Guidance & Metrics
```

**Key Principle:** GitHub Actions acts only as an execution layer. All security decisions are made by this project's logic.

## How to Run Locally

### Install dependencies
```bash
pip install pyyaml
```

### Run scanner
```bash
python scanner/secret_scanner.py
```

### Modify policy (optional)
Edit `scanner/policy.yml` to change enforcement behavior without touching code.

## CI/CD Integration

The scanner runs automatically via GitHub Actions:
- Fails pipeline if policy blocks findings
- Passes pipeline if policy allows them
- GitHub only reports the result — it does not define security logic

## Project Structure

```
DevSecOps/
├── scanner/
│   ├── secret_scanner.py
│   ├── rules.py
│   └── policy.yml
├── demo-app/
│   └── test_keys.csv
├── .github/workflows/
│   └── secret-scan.yml
├── .gitignore
└── README.md
```

## Design Philosophy

- **Detection ≠ Enforcement** – Policy controls behavior
- **Security must be explainable** – Developers understand why
- **Developer experience matters** – Better adoption
- **Metrics prove effectiveness** – Measure security posture

## Future Enhancements

- Organization-wide central policies
- Automated secret rotation
- PR comment integration
- Security scoring dashboards
- ML-assisted classification (augmentation only)

## Conclusion

This project demonstrates how DevSecOps principles can be applied to:
- Enforce security early
- Reduce human error
- Maintain flexibility via policy-as-code
- Improve developer adoption

It is CI-platform agnostic, extensible, and production-oriented.
'@ -Encoding UTF8