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

def print_pr_friendly(findings):
    print("\n🧾 SECURITY REVIEW \n")
    for idx, f in enumerate(findings, start=1):
        print(f"{idx}. ❌ **{f['type']}** ({f['severity']})")
        print(f"   - Location: `{f['file']}:{f['line']}`")
        guide = FIX_GUIDE.get(f["type"])
        if guide:
            print(f"   - Fix:")
            for step in guide["steps"]:
                print(f"     • {step}")
        print()

if __name__ == "__main__":
    policy = load_policy()
    findings = scan_repo()

    block = False
    severity_count = {}

    if findings:
        print_pr_friendly(findings)

        for f in findings:
            sev = f["severity"]
            severity_count[sev] = severity_count.get(sev, 0) + 1
            if sev in policy["block"]:
                block = True

    print("📊 SUMMARY")
    for sev, count in severity_count.items():
        print(f"- {sev}: {count}")

    if block:
        print("\n🚨 BUILD BLOCKED BY POLICY")
        exit(1)
    else:
        print("\n✅ BUILD PASSED BY POLICY")
        exit(0)
