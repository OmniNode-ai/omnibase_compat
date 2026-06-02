# Changelog

All notable changes to `omnibase_compat` should be recorded here.

This project follows semantic versioning for published package versions.

## v0.4.2 (2026-05-31)

### Changed
- fix(OMN-12254): align bifrost backend wire config (#117)
- chore(OMN-12126): add retention comments to delegation wire DTOs (#120)
- ci(OMN-12493): resolve OCC-relative DoD contract paths in Contract Compliance Check (#126)
- chore(OMN-12455): add .gitignore and untrack committed Python bytecode (#125, #127)

## v0.4.1 (2026-05-21)

### Changed
- feat(OMN-11195): add data_provenance field to EventEnvelopeV1Minimal (#92)
- feat(OMN-11262): remove contract evidence shim from omnibase_compat (#94)

### Notes
- v0.4.0 tag exists from PR #91 merge (2026-05-16) but no v0.4.0 GitHub Release was published — v0.4.1 consolidates the gap and publishes a proper Release artifact.

## Unreleased

- Documented the repo role, dependency boundary, release workflow, and docs map.
- Promoted the OMN-9459 release workflow plan into a stable runbook.
