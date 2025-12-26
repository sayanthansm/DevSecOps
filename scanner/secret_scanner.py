import os
from rules import SECRET_PATTERNS

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            for line_no, line in enumerate(f.readlines(), start=1):
                for secret_type, pattern in SECRET_PATTERNS.items():
                    if pattern.search(line):
                        findings.append({
                            "type": secret_type,
                            "file": filepath,
                            "line": line_no
                        })
    except Exception:
        pass
    return findings

def scan_repo():
    results = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".env")):
                results.extend(scan_file(os.path.join(root, file)))
    return results

if __name__ == "__main__":
    findings = scan_repo()
    if findings:
        print("\n❌ SECRET DETECTED\n")
        for f in findings:
            print(f"Type     : {f['type']}")
            print(f"File     : {f['file']}:{f['line']}")
            print("Lineage  : Hardcoded directly in source file")
            print("Fix      : Move secret to environment variable\n")
        exit(1)
    else:
        print("✅ No secrets detected")
