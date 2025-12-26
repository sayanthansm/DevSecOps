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
    files_scanned = 0

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".env", ".csv")):
                files_scanned += 1
                results.extend(scan_file(os.path.join(root, file)))

    return results, files_scanned

if __name__ == "__main__":
    findings, files_scanned = scan_repo()

    high_count = 0
    medium_count = 0

    if findings:
        print("\n🔐 SECRET ANALYSIS REPORT\n")

        for f in findings:
            print(f"Type     : {f['type']}")
            print(f"Severity : {f['severity']}")
            print(f"File     : {f['file']}:{f['line']}")
            print("Lineage  : Hardcoded directly in source file")
            print("Fix      : Move secret to environment variable\n")

            if f["severity"] == "HIGH":
                high_count += 1
            elif f["severity"] == "MEDIUM":
                medium_count += 1

    print("\n📊 SCAN SUMMARY")
    print(f"- Files scanned       : {files_scanned}")
    print(f"- HIGH-risk secrets   : {high_count}")
    print(f"- MEDIUM-risk secrets : {medium_count}")
    print(f"- Invalid ignored     : {files_scanned - (high_count + medium_count)}")

    if high_count > 0:
        print("\n🚨 BUILD BLOCKED DUE TO HIGH-RISK SECRETS")
        exit(1)
    else:
        print("\n✅ BUILD PASSED")
        exit(0)
