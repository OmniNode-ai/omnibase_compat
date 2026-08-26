# Release Workflow

The release runbook for this package now lives in the OmniNode knowledge base,
where it is maintained alongside the rest of the platform's operational
procedures.

Full documentation → https://github.com/OmniNode-ai/knowledge-base

Read it at
[runbooks/omnibase-compat-release.md](https://github.com/OmniNode-ai/knowledge-base/blob/main/runbooks/omnibase-compat-release.md).

The published version corrects two guarantees this copy omitted: the PyPI
dependency-pin resolvability check that runs before publish, and the automatic
fast-forward of `main` to the released tag on every successful non-`rc`
release.
