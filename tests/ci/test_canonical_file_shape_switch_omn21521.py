# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Canonical-file-shape node entry and ticketed first-install baseline (OMN-21521).

omnibase_compat runs omnibase_core's canonical-file-shape hook through the node
entry (``runtime_canonical_file_shape_check --rules file-shape``), pre-commit and
CI at one dev-merge tag. The findings the node entry's new rules report at the
switch commit sit in ``.onex_ratchets/canonical_file_shape_burndown_baseline.txt``
under this ticket; the repository's own shrink-only baseline is untouched.

The canary tests run the pinned hook over throwaway git repositories: a new
unbound handler is refused as ``handler_outside_node`` and a burn-down line added
after the install is refused as ``baseline-growth``.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
PRECOMMIT = REPO_ROOT / ".pre-commit-config.yaml"
BASELINE = REPO_ROOT / ".onex_ratchets" / "canonical_file_shape_baseline.txt"
BURNDOWN = REPO_ROOT / ".onex_ratchets" / "canonical_file_shape_burndown_baseline.txt"

TICKET = "OMN-21521"
CORE_TAG = "dev-20261029151319-6e0a5eee541a"
NODE_ENTRY = (
    "omnibase_core.nodes.node_canonical_file_shape_check_compute.runtime_canonical_file_shape_check"
)
RETIRED_ENTRY = "omnibase_core.validators.canonical_file_shape"


def _entries(path: Path) -> list[str]:
    return [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def _ci_core_requirement() -> str:
    match = re.search(r'CANONICAL_FILE_SHAPE_CORE:\s*"([^"]+)"', CI_WORKFLOW.read_text("utf-8"))
    assert match is not None, "ci.yml has no CANONICAL_FILE_SHAPE_CORE"
    return match.group(1)


def _precommit_hook() -> tuple[str, dict[str, object]]:
    config = yaml.safe_load(PRECOMMIT.read_text("utf-8"))
    for repo in config["repos"]:
        for hook in repo.get("hooks", []):
            if hook.get("id") == "canonical-file-shape":
                return str(repo["rev"]), hook
    raise AssertionError("no canonical-file-shape hook in .pre-commit-config.yaml")


@pytest.mark.unit
class TestSwitchWiring:
    def test_ci_and_hook_pin_one_tag(self) -> None:
        rev, _ = _precommit_hook()
        assert rev == CORE_TAG
        assert _ci_core_requirement().endswith(f"@{CORE_TAG}")

    def test_hook_runs_the_file_shape_rules(self) -> None:
        _, hook = _precommit_hook()
        assert hook.get("args") == ["--rules", "file-shape"]

    def test_ci_runs_only_the_node_entry(self) -> None:
        text = CI_WORKFLOW.read_text("utf-8")
        assert RETIRED_ENTRY not in text
        invocations = re.findall(rf"-m {re.escape(NODE_ENTRY)}([^\n]*)", text)
        assert len(invocations) == 3
        assert all(arg.startswith(" --rules file-shape") for arg in invocations)

    def test_no_placeholder_token_is_left(self) -> None:
        for path in (CI_WORKFLOW, PRECOMMIT):
            assert "TAG-PENDING" not in path.read_text("utf-8")


@pytest.mark.unit
class TestBurndownBaseline:
    def test_header_names_this_ticket(self) -> None:
        first = BURNDOWN.read_text("utf-8").splitlines()[0]
        assert first.startswith(f"# Burn-down ticket: {TICKET}")

    def test_entries_are_existing_files_the_baseline_does_not_list(self) -> None:
        entries = _entries(BURNDOWN)
        assert entries == sorted(set(entries))
        assert not set(entries) & set(_entries(BASELINE))
        for entry in entries:
            assert (REPO_ROOT / entry).is_file(), f"{entry} no longer exists: delete its line"


def _git(repo: Path, *args: str) -> None:
    git = shutil.which("git")
    assert git is not None, "git is required to build the canary repository"
    subprocess.run(
        [git, "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def _commit_all(repo: Path, message: str) -> None:
    _git(repo, "add", "-A")
    _git(
        repo,
        "-c",
        "user.email=canary@example.invalid",
        "-c",
        "user.name=canary",
        "commit",
        "-q",
        "-m",
        message,
    )


def _run_hook(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    uv = shutil.which("uv")
    assert uv is not None, "uv is required to run the pinned hook"
    return subprocess.run(
        [
            uv,
            "run",
            "--no-project",
            "--with",
            _ci_core_requirement(),
            "python",
            "-m",
            NODE_ENTRY,
            "--rules",
            "file-shape",
            "--repo-root",
            str(repo),
            *args,
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo,
    )


def _seed_repo(root: Path) -> Path:
    repo = root / "repo"
    (repo / ".onex_ratchets").mkdir(parents=True)
    (repo / "src" / "pkg" / "models").mkdir(parents=True)
    (repo / "scripts").mkdir()
    _git(repo, "init", "-q", "-b", "dev")
    (repo / "pyproject.toml").write_text('[project]\nname = "pkg"\nversion = "0"\n')
    (repo / "src" / "pkg" / "models" / "model_a.py").write_text("x = 1\n")
    (repo / "scripts" / "a.py").write_text("x = 1\n")
    (repo / "scripts" / "b.sh").write_text("#!/bin/sh\n")
    (repo / ".onex_ratchets" / "canonical_file_shape_baseline.txt").write_text(
        "# canonical-file-shape baseline. Shrink-only.\nscripts/a.py\n"
    )
    (repo / ".onex_ratchets" / "canonical_file_shape_burndown_baseline.txt").write_text(
        f"# Burn-down ticket: {TICKET}\nscripts/b.sh\n"
    )
    _commit_all(repo, f"{TICKET}: seed")
    return repo


@pytest.mark.integration
class TestRatchetHolds:
    def test_seed_repo_is_accepted(self, tmp_path: Path) -> None:
        repo = _seed_repo(tmp_path)
        result = _run_hook(repo, "--head", "HEAD")
        assert result.returncode == 0, result.stdout + result.stderr

    def test_new_unbound_handler_is_refused(self, tmp_path: Path) -> None:
        repo = _seed_repo(tmp_path)
        handlers = repo / "src" / "pkg" / "handlers"
        handlers.mkdir()
        (handlers / "handler_zz_canary.py").write_text(
            "class Handler:\n    def handle(self, request: int) -> int:\n        return request\n"
        )
        _git(repo, "add", "-A")
        result = _run_hook(repo)
        assert result.returncode == 1, result.stdout + result.stderr
        assert "[handler_outside_node]" in result.stdout + result.stderr

    def test_burndown_line_for_an_existing_refused_file_is_refused(self, tmp_path: Path) -> None:
        repo = _seed_repo(tmp_path)
        ratchets = repo / ".onex_ratchets"
        (ratchets / "canonical_file_shape_baseline.txt").write_text(
            "# canonical-file-shape baseline. Shrink-only.\n"
        )
        (ratchets / "canonical_file_shape_burndown_baseline.txt").write_text(
            f"# Burn-down ticket: {TICKET}\nscripts/a.py\nscripts/b.sh\n"
        )
        _commit_all(repo, f"{TICKET}: move a baseline line into the burn-down file")
        result = _run_hook(repo, "--base", "HEAD~1", "--head", "HEAD")
        assert result.returncode == 1, result.stdout + result.stderr
        assert "[baseline-growth]" in result.stdout + result.stderr
