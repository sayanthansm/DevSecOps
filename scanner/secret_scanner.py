import os
import yaml
from rules import SECRET_PATTERNS

POLICY_FILE = "scanner/policy.yml"

FIX_GUIDE = {
    "AWS Access Key": {
        "env": "AWS_ACCESS_KEY_ID",
        "steps": [
            "Remove hardcoded AWS key from source code",
            "Add AWS_ACCESS_KEY_ID to GitHub Secrets",
            "Access it using os.getenv('AWS_ACCESS_KEY_ID')"
        ]
    },
    "Generic API Key": {
        "env": "API_KEY",
        "steps": [
            "Remove hardcoded API key",
            "Add API_KEY to environment variables",
            "Access it using os.getenv('API_KEY')"
        ]
    }
}

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
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".env", ".csv")):
                results.extend(scan_file(os.path.join(root, file)))
    return results

if __name__ == "__main__":
    policy = load_policy()
    findings = scan_repo()

    block = False
    severity_count = {}

    if findings:
        print("\n🔐 SECRET ANALYSIS REPORT\n")

        for f in findings:
            sev = f["severity"]
            severity_count[sev] = severity_count.get(sev, 0) + 1

            print(f"❌ Secret Type : {f['type']}")
            print(f"   Severity   : {sev}")
            print(f"   Location   : {f['file']}:{f['line']}")

            guide = FIX_GUIDE.get(f["type"])
            if guide:
                print("   Suggested Fix:")
                for step in guide["steps"]:
                    print(f"     - {step}")
            print()

            if sev in policy["block"]:
                block = True

    print("📊 SCAN SUMMARY")
    for sev, count in severity_count.items():
        print(f"- {sev} secrets : {count}")

    if block:
        print("\n🚨 BUILD BLOCKED — FIX REQUIRED")
        exit(1)
    else:
        print("\n✅ BUILD PASSED — POLICY SATISFIED")
        exit(0)
