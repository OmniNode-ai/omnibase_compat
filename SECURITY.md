# Security

## Supported Versions

Security fixes are handled on the latest published version unless a release owner
explicitly opens a backport branch.

## Reporting

Report security issues privately to the repository maintainers. Do not open a
public issue for suspected vulnerabilities.

## Package Boundary

`omnibase_compat` is a structural package. It must not contain:

- Network clients
- Persistence clients
- Secret loading logic
- Runtime orchestration
- Privileged host operations

Those responsibilities belong in canonical runtime or infrastructure repos.

## Validation

Before release, run:

```bash
uv run python scripts/validate_no_upstream_deps.py
uv run python scripts/check_compat_retention.py
uv build
```

