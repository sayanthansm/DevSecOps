import re

SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "JWT Token": re.compile(r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\."),
    "Generic API Key": re.compile(
        r"(api[_-]?key|secret|token)\s*=\s*[\"'][A-Za-z0-9_-]{16,}[\"']",
        re.IGNORECASE
    )
}
