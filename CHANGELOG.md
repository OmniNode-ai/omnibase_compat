# Changelog

All notable changes to `omnibase_compat` should be recorded here.

This project follows semantic versioning for published package versions.

## v0.5.5 (2026-06-30)

### Added
- feat: migrate env read + URL literal to contract/overlay (OMN-13564, #159)
- feat: wire validate-validator-requirements fleet gate (OMN-13291, #156)

### Changed
- docs: sanitize documentation — strip local-env traces and OMN-XXXX refs (OMN-13570, #158)
- docs: refresh architecture docs verified against code (OMN-13463, #157)
- docs: refresh omnibase_compat documentation (OMN-13176, #155)

## v0.5.4 (2026-06-11)

### Changed
- ci: promote dev integration to main; backmerge release metadata (#146, #147)

### Added
- feat: non-dev-base guard — fail feature-base PRs absent Stacked-Parent declaration (#151)
- ci: wire receipt-honesty gate as required CI ratchet (#148)

## v0.5.3 (2026-06-10)

### Changed
- release: promote compat dev lane to main; backmerge release evidence (#137, #139, #141, #143)

## v0.5.2 (2026-06-06)

### Added
- chore: delete dead `contracts/delegation/wire/` shim module (#132); consumers must import from `contracts/delegation/` directly.
- feat: add `scripts/check_no_infra_edge.py` closure guard; wire as pre-commit hook scanning `pyproject.toml` and `uv.lock` for forbidden upstream edges (#131)
- feat: mirror runtime deployment wire DTOs in `contracts/runtime_deployment/wire/` (#129)

### Changed
- ci: resolve OCC-relative DoD contract paths in Contract Compliance Check (#126)
- chore: add `.gitignore`; untrack committed Python bytecode (#125, #127)

## v0.5.1 (2026-05-30)

### Fixed
- fix: release delegation escalation DTOs (#121)
- ci: add main target guard (#119)
- chore: add retention comments to delegation wire DTOs (#120)

## v0.5.0 (2026-05-22)

### Added
- feat: wire `contract.yaml` topic definitions for evidence pipeline (#107)
- feat: add evidence dashboard DTOs to `contracts/evidence_pipeline/wire/`
- feat: add evidence pipeline wire DTOs (`model_evidence_pipeline_command`, `model_evidence_bundle`, `model_gap_report`, `model_occ_pr_reference`, `topics`, `types`) (#98)
- feat: add contract evidence storage models to `contracts/evidence/` (#100)
- feat: add `api_key` / `extra_headers` to delegation wire models (#108)
- feat: add `min_success_rate` to `ModelTierModel` (#110)
- feat: add `min_tier_name` field to `ModelRoutingIntent` for tier escalation (#113)
- feat: add delegation escalation terminal metadata; export delegation quality contract helpers; align delegation runtime wire fields and bifrost backend wire config (#115, #116, #117)

### Fixed
- fix: add `api_key_env`, `extra_headers`; make `model_name` and `endpoint_url` optional in `ModelDelegationBackendConfig` (#109)
- fix: fix compat retention CI failure

### Changed
- ci: propagate skip-token rejection hook from `omniclaude` (#96)
- ci: add `edited` trigger to receipt-gate caller workflow (#97)
- ci: support `dev` and `hotfix` workflow triggers (#104)

## v0.4.2 (2026-05-31)

### Changed
- fix: align bifrost backend wire config (#117)
- chore: add retention comments to delegation wire DTOs (#120)
- ci: resolve OCC-relative DoD contract paths in Contract Compliance Check (#126)
- chore: add .gitignore and untrack committed Python bytecode (#125, #127)

## v0.4.1 (2026-05-21)

### Changed
- feat: add data_provenance field to EventEnvelopeV1Minimal (#92)
- feat: remove contract evidence shim from omnibase_compat (#94)

### Notes
- v0.4.0 tag exists from PR #91 merge (2026-05-16) but no v0.4.0 GitHub Release was published — v0.4.1 consolidates the gap and publishes a proper Release artifact.

## Unreleased

- Documented the repo role, dependency boundary, release workflow, and docs map.
- Promoted the release workflow plan into a stable runbook.
