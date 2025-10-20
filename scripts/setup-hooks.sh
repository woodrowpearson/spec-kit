#!/bin/bash
set -euo pipefail

HOOK=".git/hooks/pre-commit"
cat > "$HOOK" <<'EOF'
#!/bin/bash
python3 scripts/lint-specs.py || exit 1
EOF
chmod +x "$HOOK"
echo "Installed pre-commit hook"
