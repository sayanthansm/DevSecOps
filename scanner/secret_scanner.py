import os
import yaml
from rules import SECRET_PATTERNS

CI_AUDIT_MODE = os.getenv("CI_AUDIT_MODE", "false").lower() == "true"

LAST_SCAN_FILE = "scanner/.last_scan.yml"


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
            full_path = os.path.join(root, file)

            # Skip test data explicitly
            if full_path.endswith("test_keys.csv"):
                continue

            if file.endswith((".py", ".js", ".env")):
                results.extend(scan_file(full_path))
    return results


def load_last_scan():
    if not os.path.exists(LAST_SCAN_FILE):
        return {}
    with open(LAST_SCAN_FILE, "r") as f:
        return yaml.safe_load(f) or {}

def save_current_scan(summary):
    with open(LAST_SCAN_FILE, "w") as f:
        yaml.safe_dump(summary, f)


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

        current_summary = severity_count
    last_summary = load_last_scan()

       # Prepare summaries
    current_summary = severity_count
    last_summary = load_last_scan()

    print("\n🔄 SECURITY CHANGE SUMMARY")
    for sev in set(current_summary.keys()).union(last_summary.keys()):
        prev = last_summary.get(sev, 0)
        curr = current_summary.get(sev, 0)
        if curr > prev:
            print(f"⚠ {sev} increased: {prev} → {curr}")
        elif curr < prev:
            print(f"✅ {sev} reduced: {prev} → {curr}")
        else:
            print(f"• {sev} unchanged: {curr}")

    # Save scan summary for next run comparison
    save_current_scan(current_summary)

    # Final enforcement decision
    if block and not CI_AUDIT_MODE:
        print("\n🚫 Build blocked due to high severity findings.")
        exit(1)
    else:
        if CI_AUDIT_MODE:
            print("\nℹ CI running in AUDIT mode — enforcement skipped")
        print("\n✅ Build can proceed.")
        exit(0)

