import re

SECRET_PATTERNS = {
    "AWS Access Key": {
        "pattern": re.compile(r"AKIA[0-9A-Z]{16}"),
        "severity": "HIGH"
    },
    "Generic API Key": {
        "pattern": re.compile(
            r"(api[_-]?key|secret|token)\s*=\s*[\"'][A-Za-z0-9_-]{16,}[\"']",
            re.IGNORECASE
        ),
        "severity": "MEDIUM"
    }
}
