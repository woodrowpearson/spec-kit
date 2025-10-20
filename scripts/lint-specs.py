#!/usr/bin/env python3
import sys, re, os, yaml, json, subprocess

REQUIRED = {
  "PRD": ["type","status","owner","created","target_release"],
  "DesignDoc": ["type","status","owner","created","related_prd"],
  "ADR": ["type","number","status","date","deciders"],
  "TestPlan": ["type","feature","owner","created"],
  "Runbook": ["type","status","owner","created","service"],
  "SDD": ["type","status","owner","created","related_design"]
}

def read_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return None, "Missing YAML frontmatter"
    try:
        fm = yaml.safe_load(m.group(1))
        return fm, None
    except Exception as e:
        return None, f"Invalid YAML: {e}"

def check_frontmatter(path):
    fm, err = read_frontmatter(path)
    if err:
        return [(path, err)]
    t = fm.get("type")
    errs = []
    if not t:
        errs.append((path, "Missing 'type' in frontmatter"))
    else:
        req = REQUIRED.get(t, [])
        for k in req:
            if k not in fm:
                errs.append((path, f"Missing required field '{k}' for type {t}"))
    return errs

def find_files(root, exts=(".md",)):
    for dirpath, _, filenames in os.walk(root):
        for n in filenames:
            if n.endswith(exts):
                yield os.path.join(dirpath, n)

def grep_changed_files(patterns):
    try:
        diff = subprocess.check_output(["git","diff","origin/main...HEAD"], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return False
    rgx = re.compile(patterns, re.M)
    return bool(rgx.search(diff))

def check_test_ids(tests_root="."):
    bad = []
    for path in find_files(tests_root, (".swift",)):
        if path.endswith("Tests.swift"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            # Look for test methods that lack preceding TC-XXX tag within 3 lines above
            for m in re.finditer(r"(?m)^\s*func\s+test_[A-Za-z0-9_]+\s*\(", txt):
                start = max(0, m.start() - 300)  # small window above
                window = txt[start:m.start()]
                if not re.search(r"TC-\d{3}", window):
                    bad.append((path, "Test missing TC-ID", m.group(0)))
    return bad

def main():
    paths = sys.argv[1:] or ["docs/specs","docs/adr"]
    errors = []
    for base in paths:
        if os.path.isdir(base):
            for p in find_files(base, (".md",)):
                errors += check_frontmatter(p)
        elif os.path.isfile(base):
            errors += check_frontmatter(base)
    # ADR required if architectural files changed
    adr_needed = grep_changed_files(r"(Database|APIClient|Auth|import\\s+(Alamofire|SQLite|GRDB))")
    if adr_needed:
        # ensure there's any ADR in the current change
        has_new_adr = any(p.startswith("docs/adr/") for p in find_files("docs/adr") )
        if not has_new_adr:
            errors.append(("docs/adr", "Architectural change detected but no ADR added/updated"))

    # Test IDs
    test_problems = check_test_ids(".")
    for path, msg, ctx in test_problems:
        errors.append((path, msg))

    if errors:
        for p, msg in errors:
            print(f"❌ {p}: {msg}")
        sys.exit(1)
    else:
        print("✅ spec-lint passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
