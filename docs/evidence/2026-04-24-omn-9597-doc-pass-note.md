# OMN-9597 Doc Pass Note

**Issue:** OMN-9597
**Parent:** OMN-9594
**Date:** 2026-04-24
**Scope:** `omnibase_compat` entrypoint, docs index, release runbook, and repo metadata.

## Dirty Worktree Snapshot

Command:

```bash
git status --short
```

Output at start of pass:

```text
 M src/omnibase_compat/__pycache__/__init__.cpython-312.pyc
 M src/omnibase_compat/routing/__pycache__/__init__.cpython-312.pyc
 M src/omnibase_compat/routing/__pycache__/model_routing_degraded_event.cpython-312.pyc
 M src/omnibase_compat/routing/__pycache__/model_routing_policy.cpython-312.pyc
 M src/omnibase_compat/telemetry/__pycache__/__init__.cpython-312.pyc
 M src/omnibase_compat/telemetry/__pycache__/model_post_mortem_report.cpython-312.pyc
 M src/omnibase_compat/telemetry/__pycache__/model_session_bootstrap_result.cpython-312.pyc
?? omnibase_compat
?? src/omnibase_compat/concurrency/__pycache__/
?? src/omnibase_compat/overseer/__pycache__/
?? src/omnibase_compat/telemetry/__pycache__/model_sweep_result.cpython-312.pyc
```

These are generated/cache artifacts plus an existing self-referential symlink.
They were not edited or cleaned as part of this documentation pass.

## Entrypoints Reviewed

- `README.md`
- `CLAUDE.md`
- `AGENT.md`
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `docs/plans/omn-9459-release-workflow.md`
- `scripts/validate_no_upstream_deps.py`
- `scripts/check_compat_retention.py`

## Canonical Docs Added Or Updated

- `README.md`
- `docs/README.md`
- `docs/runbooks/release.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `LICENSE`

## Promotion Decisions

- `docs/plans/omn-9459-release-workflow.md` remains historical execution context.
- `docs/runbooks/release.md` is the stable release runbook.

## Validation Result

No-upstream-dependency validator:

```text
OK - scanned 57 files, no forbidden imports.
```

Compat retention validator:

```text
OK - scanned 57 files, no stale compat modules.
```

Unit subset:

```text
17 passed, 40 deselected in 0.28s
```

Docs link validator:

```text
error: Failed to spawn: `onex-validate-links`
  Caused by: No such file or directory (os error 2)
```

This is expected for this pass: `omnibase_compat` does not currently expose the
shared docs-validator entrypoint, and OMN-9597 explicitly preserves the rule
that `omnibase_compat` must not consume `omnibase_core` just to validate docs.
Full docs-validation wiring is tracked by OMN-9607.

Running the validation commands created or updated additional `__pycache__`
artifacts in the already-dirty worktree. They are generated files and were not
included in the documentation change.
