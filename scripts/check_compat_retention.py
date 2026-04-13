#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Check that all compat modules have a COMPAT_REMOVAL_DATE comment.

Any .py file under src/omnibase_compat/ that defines a class and was committed
more than 30 days ago must carry:

    # COMPAT_MIGRATION_TARGET: <canonical.module.path>
    # COMPAT_REMOVAL_DATE: YYYY-MM-DD

Exits 1 if stale modules are found (missing removal date, or removal date passed).

Run: python scripts/check_compat_retention.py
"""

import ast
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

SRC = Path("src/omnibase_compat")
SKIP_FILES = {"__init__.py"}
SKIP_MARKER = "compat-skip-retention:"
REMOVAL_DATE_RE = re.compile(r"#\s*COMPAT_REMOVAL_DATE:\s*(\d{4}-\d{2}-\d{2})")
STALE_THRESHOLD_DAYS = 30


def get_file_commit_date(path: Path) -> date | None:
    """Return the earliest commit date for a file, or None if untracked."""
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%aI", "--", str(path)],
        capture_output=True,
        text=True,
    )
    lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    # Last line = oldest commit
    oldest = lines[-1]
    return datetime.fromisoformat(oldest).date()


def has_skip_marker(text: str) -> bool:
    return any(SKIP_MARKER in line for line in text.splitlines()[:10])


def has_class_definition(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    return any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))


violations: list[str] = []
today = date.today()

for py_file in SRC.rglob("*.py"):
    if py_file.name in SKIP_FILES:
        continue

    text = py_file.read_text(encoding="utf-8")

    if has_skip_marker(text):
        continue

    if not has_class_definition(py_file):
        continue

    commit_date = get_file_commit_date(py_file)
    if commit_date is None:
        # Untracked file — skip (not yet committed)
        continue

    days_old = (today - commit_date).days

    match = REMOVAL_DATE_RE.search(text)

    if match is None:
        if days_old > STALE_THRESHOLD_DAYS:
            violations.append(
                f"{py_file}: no COMPAT_REMOVAL_DATE comment"
                f" (committed {days_old} days ago, threshold {STALE_THRESHOLD_DAYS})"
            )
    else:
        removal_date = date.fromisoformat(match.group(1))
        if removal_date < today:
            violations.append(
                f"{py_file}: COMPAT_REMOVAL_DATE {removal_date} has passed"
                f" (today is {today}) — migrate or extend the date"
            )

if violations:
    print("FAIL — stale compat modules found:")
    for v in violations:
        print(f"  {v}")
    print()
    print(
        "Each compat module with class definitions must carry:\n"
        "  # COMPAT_MIGRATION_TARGET: <canonical.module.path>\n"
        "  # COMPAT_REMOVAL_DATE: YYYY-MM-DD\n"
        "Or add '# compat-skip-retention: <reason>' in the first 10 lines to exempt."
    )
    sys.exit(1)

count = sum(1 for _ in SRC.rglob("*.py"))
print(f"OK — scanned {count} files, no stale compat modules.")
