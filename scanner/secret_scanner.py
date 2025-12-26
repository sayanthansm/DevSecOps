import os
from rules import SECRET_PATTERNS

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            for line_no, line in enumerate(f.readlines(), start=1):
                for secret_type, meta in SECRET_PATTERNS.items():
                    if meta["pattern"].search(line):
                        findings.append({
                            "type": secret_type,
                            "severity": meta["severity"],
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

    if not findings:
        print("✅ No secrets detected")
        exit(0)

    print("\n🔐 SECRET ANALYSIS REPORT\n")

    high_risk_found = False

    for f in findings:
        print(f"Type     : {f['type']}")
        print(f"Severity : {f['severity']}")
        print(f"File     : {f['file']}:{f['line']}")
        print("Lineage  : Hardcoded directly in source file")
        print("Fix      : Move secret to environment variable\n")

        if f["severity"] == "HIGH":
            high_risk_found = True

    if high_risk_found:
        print("🚨 HIGH-RISK SECRET DETECTED — BUILD BLOCKED")
        exit(1)
    else:
        print("⚠️ MEDIUM-RISK SECRET DETECTED — WARNING ONLY")
        exit(0)
