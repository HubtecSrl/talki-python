# talki-python

The Python SDK for Talki's public API, published to PyPI as `talki` (import name
`talki`). MIT. This repo will be public: write every file, commit message and PR
for an outside reader. No internal hostnames, people, PR numbers of private repos,
or customer names.

## Where things come from

- `openapi/talki-v1.yaml` is a pinned copy of the spec that `talki-backend` exports
  and commits at `api-cli/openapi/talki-v1.yaml`. Refresh it with
  `uv run scripts/pull_spec.py`. It reads the sibling backend checkout's `origin/main`,
  which is what production serves. Never release from a `--ref origin/dev` pull.
  A wrong or missing schema is fixed in the backend, never here.
- `talki/` is mostly generated: `uv run scripts/generate.py` runs
  openapi-python-client (pinned in `pyproject.toml`) with `codegen/config.yaml`
  and `codegen/templates/`, then formats the output with this repo's ruff
  settings. Never hand-edit a generated file. Change a template or the config, then
  regenerate. CI fails on drift (`generate.py --check`).
- The hand-written modules are listed in `HAND_WRITTEN` in `scripts/generate.py`:
  `_talki.py`, `_transport.py`, `exceptions.py`, `oauth.py`, `pagination.py`,
  `webhooks.py`, `py.typed`. Edit them in place. A new hand-written module must
  be added to that list, or the next regeneration deletes it.
- Each template in `codegen/templates/` is a copy of the upstream 0.29.1
  template with one marked change, described in its header comment. On a
  generator upgrade, re-copy them and re-apply the changes.

## Who else builds from this repo

`talki-backend`'s `api-cli` (its internal test tool) builds its client from the
backend branch's own spec with `scripts/generate.py --spec … --out …`, at a
pinned tag of this repo. So the `--out` mode and the script's interface are a
contract: change them only with a backend PR that bumps the pin.

The backend also keeps a test that checks `talki.webhooks` against the server's
real signer. Here, `tests/test_webhooks.py` checks against a reference signer in
the documented format.

## Checks

```sh
uv sync
uv run ruff check . && uv run ruff format --check .
uv run mypy                    # strict, on talki/
uv run pytest
uv run scripts/generate.py --check
```

CI (`.github/workflows/ci.yml`) runs these on Python 3.11–3.14, plus 3.11 with
the lowest declared dependencies, on GitHub-hosted runners only. This repo
takes fork PRs, so it must never use self-hosted runners.

## Releasing

1. Move the `CHANGELOG.md` entry from "unreleased" to the date, bump `version`
   in `pyproject.toml`, and merge.
2. Tag `v<version>` on `main` and push the tag. `release.yml` checks that the tag
   matches, tests, builds, publishes to PyPI by trusted publishing (the `pypi`
   environment), and creates the GitHub release.

The package uses semver of its own. `talki.API_VERSION` (the spec's dated
version) is what it sends as `Talki-Version` by default. Moving to a newer API
version is a changelog line, and a major bump if it breaks callers.

## Working rules

- `main` is the only branch. Work on a feature branch and open a PR into `main`.
  Merge only when the maintainer says so, and never push a release tag without asking.
- Run a code-review agent before every push, fix, re-test.
- Commit only your own paths (`git commit -- <paths>`).
