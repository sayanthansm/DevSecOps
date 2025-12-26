import os
import yaml
from rules import SECRET_PATTERNS

POLICY_FILE = "scanner/policy.yml"

def load_policy():
    with open(POLICY_FILE, "r") as f:
        return yaml.safe_load(f)["enforcement"]

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
    policy = load_policy()
    findings, files_scanned = scan_repo()

    severity_count = {}
    block_build = False

    if findings:
        print("\n🔐 SECRET ANALYSIS REPORT\n")

        for f in findings:
            sev = f["severity"]
            severity_count[sev] = severity_count.get(sev, 0) + 1

            print(f"Type     : {f['type']}")
            print(f"Severity : {sev}")
            print(f"File     : {f['file']}:{f['line']}")
            print("Fix      : Move secret to environment variable\n")

            if sev in policy["block"]:
                block_build = True

    print("\n📊 SCAN SUMMARY")
    print(f"- Files scanned : {files_scanned}")
    for sev, count in severity_count.items():
        print(f"- {sev} secrets : {count}")

    if block_build:
        print("\n🚨 BUILD BLOCKED BY POLICY")
        exit(1)
    else:
        print("\n✅ BUILD PASSED BY POLICY")
        exit(0)
