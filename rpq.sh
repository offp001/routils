#!/usr/bin/env bash
set -Eeuo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'ERROR: Run this script from inside the cloned RoUtils Git repository.\n' >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

printf '\n=== RoUtils repository preflight ===\n'
printf 'Repository: %s\n' "$ROOT"
printf '\n--- Git status (before) ---\n'
git status --short
printf '\n--- Root files ---\n'
find . -maxdepth 1 -mindepth 1 -printf '%f\n' | sort
printf '\n--- Existing dependency file ---\n'
if [[ -f requirements.txt ]]; then
  sed -n '1,200p' requirements.txt
else
  printf 'requirements.txt not found.\n'
fi
printf '\n--- Protected documentation ---\n'
for f in README.md CONTRIBUTING.md; do
  if [[ -f "$f" ]]; then printf 'Found: %s\n' "$f"; else printf 'Not found: %s\n' "$f"; fi
done

printf '\nThis script creates only missing files. It will not edit README.md or CONTRIBUTING.md,\nand it will not commit or push anything.\n'
read -r -p 'Continue with creating missing repository-quality files? [y/N] ' answer
case "$answer" in y|Y|yes|YES) ;; *) printf 'Cancelled; no files created.\n'; exit 0 ;; esac

created=()
skipped=()
create_if_missing() {
  local path="$1"
  local dir
  dir="$(dirname "$path")"
  mkdir -p "$dir"
  if [[ -e "$path" ]]; then
    skipped+=("$path")
    printf 'SKIP (already exists): %s\n' "$path"
    cat >/dev/null
  else
    cat > "$path"
    created+=("$path")
    printf 'CREATED: %s\n' "$path"
  fi
}

create_if_missing .gitignore <<'EOF'
# Python bytecode and caches
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/
env/
ENV/

# Build and packaging output
build/
dist/
*.egg-info/

# Local configuration and secrets
.env
.env.*
!.env.example
*.pem
*.key

# Logs and temporary files
*.log
*.tmp
*.bak

# Editors and operating systems
.idea/
.vscode/
*.swp
*.swo
.DS_Store
Thumbs.db

# Local test and tool output
.pyre/
.hypothesis/
EOF

create_if_missing .editorconfig <<'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
trim_trailing_whitespace = true

[*.{yml,yaml,json,toml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[*.{bat,cmd,ps1}]
end_of_line = crlf
EOF

create_if_missing SECURITY.md <<'EOF'
# Security Policy

## Reporting a Vulnerability

Please do not publish credentials, API keys, private user data, or unpatched security vulnerabilities in public issues.

For a suspected security issue, contact the project maintainer privately through a contact method listed on the official RoUtils GitHub profile or repository. Include a concise description, steps to reproduce, the affected version or commit, and the potential impact. Avoid attaching real credentials or other sensitive data.

If no private reporting channel is available, open a minimal GitHub issue asking for a private contact method without disclosing the vulnerability details.

## Scope

Reports are most useful when they identify a reproducible security impact in RoUtils itself. This policy does not promise a particular response time or that every report will result in a security release.

## Safe Testing

Only test software and systems you own or have explicit permission to test. Do not access, modify, or disclose another person's data.
EOF

create_if_missing CHANGELOG.md <<'EOF'
# Changelog

Notable changes to RoUtils are documented here.

This project uses a human-maintained changelog. Entries should describe user-visible changes and reference the relevant release or commit when practical.

## Unreleased

- Repository quality and contributor tooling may be added in this section after review and verification.
EOF

create_if_missing CODE_OF_CONDUCT.md <<'EOF'
# Code of Conduct

## Our Standard

Contributors and community members are expected to be respectful, constructive, and welcoming. Harassment, personal attacks, discriminatory conduct, and deliberate disruption are not acceptable.

## Expected Behaviour

- Be considerate and respectful when discussing ideas and code.
- Give actionable feedback focused on the work, not the person.
- Accept constructive criticism and differing viewpoints.
- Respect the privacy and security of other people.

## Unacceptable Behaviour

- Harassment, threats, insults, or discriminatory language.
- Publishing private information without permission.
- Deliberately derailing discussions or repeatedly disrupting project spaces.

## Reporting

Report conduct concerns to the project maintainer through a private contact method listed on the official RoUtils GitHub profile or repository. Include relevant context without publicly exposing private information.

The maintainer will review reports and determine an appropriate response based on the circumstances.
EOF

create_if_missing DEPENDENCIES.md <<'EOF'
# Dependencies

## Source of Truth

Check `requirements.txt` and the import statements in the source code before installing or changing dependencies. Keep this document descriptive; do not assume every optional feature requires every package.

## Development

- Python: use the version required by the current project and its supported platform.
- Git: required to clone the repository and inspect changes.
- Pytest: used by the repository test workflow.

## Runtime Dependencies

Install the project's declared dependencies with:

```bash
python -m pip install -r requirements.txt
```

Some features may rely on optional or platform-specific packages. Verify those requirements against the corresponding feature code and the current installation instructions before changing the dependency list.

## Dependency Changes

- Add a package to the dependency manifest only when the application actually needs it.
- Check supported Python versions and operating systems before upgrading a package.
- Avoid committing local virtual environments, downloaded artifacts, credentials, or machine-specific configuration.
- Run the available tests after dependency changes.
EOF

create_if_missing pyproject.toml <<'EOF'
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
EOF

create_if_missing .github/workflows/ci.yml <<'EOF'
name: CI

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  python-checks:
    name: Python checks
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install test runner
        run: python -m pip install --upgrade pip pytest

      - name: Check main module syntax
        run: python -m compileall -q main.pyw

      - name: Run repository tests
        run: python -m pytest
EOF

create_if_missing tests/test_repository_sanity.py <<'EOF'
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_main_entrypoint_exists() -> None:
    assert (ROOT / "main.pyw").is_file(), "Expected main.pyw at the repository root"


def test_dependency_manifest_exists() -> None:
    assert (ROOT / "requirements.txt").is_file(), "Expected requirements.txt at the repository root"


def test_readme_and_contributing_are_preserved() -> None:
    assert (ROOT / "README.md").is_file(), "README.md is missing"
    assert (ROOT / "CONTRIBUTING.md").is_file(), "CONTRIBUTING.md is missing"
EOF

printf '\n=== Created files ===\n'
if ((${#created[@]})); then printf '  %s\n' "${created[@]}"; else printf '  No new files created.\n'; fi
printf '\n=== Existing files left untouched ===\n'
if ((${#skipped[@]})); then printf '  %s\n' "${skipped[@]}"; else printf '  None.\n'; fi

printf '\n=== Validation ===\n'
validation_failed=0
if [[ -f main.pyw ]]; then
  if python -m compileall -q main.pyw; then printf 'PASS: main.pyw syntax compilation\n'; else printf 'FAIL: main.pyw syntax compilation\n'; validation_failed=1; fi
else
  printf 'SKIP: main.pyw not found; verify the project entry point.\n'
fi

if python -m pytest --version >/dev/null 2>&1; then
  if python -m pytest -q; then printf 'PASS: pytest\n'; else printf 'FAIL: pytest\n'; validation_failed=1; fi
else
  printf 'SKIP: pytest is not installed in the current Python environment.\n'
  printf 'Install it in your environment with: python -m pip install pytest\n'
fi

if git diff --check; then printf 'PASS: git diff --check (tracked files)\n'; else printf 'FAIL: git diff --check\n'; validation_failed=1; fi

printf '\n=== Tracked-file diff ===\n'
git diff --

printf '\n=== New-file previews (untracked files are not shown by plain git diff) ===\n'
for f in "${created[@]}"; do
  printf '\n--- %s ---\n' "$f"
  git diff --no-index -- /dev/null "$f" || [[ $? -eq 1 ]]
done

printf '\n=== Git status (after) ===\n'
git status --short

printf '\n=== Protected documentation check ===\n'
if git diff --quiet -- README.md CONTRIBUTING.md; then
  printf 'PASS: no tracked changes to README.md or CONTRIBUTING.md\n'
else
  printf 'WARNING: README.md or CONTRIBUTING.md has tracked changes; inspect git status before proceeding.\n'
  validation_failed=1
fi

printf '\nNo commit or push was performed. Review the diff before staging anything.\n'
exit "$validation_failed"
