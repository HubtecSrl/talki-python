"""Refresh the pinned OpenAPI document, `openapi/talki-v1.yaml`.

The API's own repository exports the document and commits it at
`api-cli/openapi/talki-v1.yaml`. With no argument this reads that file from
the sibling `talki-backend` checkout's `origin/main`, freshly fetched: the
contract production serves, whichever branch that checkout has out. Only
Talki's team has that checkout; anyone else passes a path or URL.

    uv run scripts/pull_spec.py
    uv run scripts/pull_spec.py --ref origin/dev      # preview; never release from it
    uv run scripts/pull_spec.py ./talki-v1.yaml
    uv run scripts/pull_spec.py https://developers.talki.it/openapi.yaml

`TALKI_BACKEND` names the backend checkout when it is not the sibling
directory. Then run `uv run scripts/generate.py`.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "openapi" / "talki-v1.yaml"
SPEC_IN_BACKEND = "api-cli/openapi/talki-v1.yaml"


def _git(backend: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(backend), *args], capture_output=True, encoding="utf-8")
    if done.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed in {backend}:\n{done.stderr}")
    return done.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", nargs="?", help="a path or http(s) URL instead of the backend checkout")
    parser.add_argument("--ref", default="origin/main", help="the backend commit to read (default: %(default)s)")
    args = parser.parse_args()

    if args.source and args.source.startswith(("http://", "https://")):
        with urllib.request.urlopen(args.source, timeout=30) as answer:
            text = answer.read().decode()
        origin = args.source
    elif args.source:
        text = Path(args.source).read_text(encoding="utf-8")
        origin = args.source
    else:
        backend = Path(os.environ.get("TALKI_BACKEND", ROOT.parent / "talki-backend")).expanduser()
        rev = args.ref
        if rev.startswith("origin/"):
            # FETCH_HEAD, not the remote-tracking ref, which a narrowed clone may not update.
            _git(backend, "fetch", "--quiet", "origin", rev.removeprefix("origin/"))
            rev = "FETCH_HEAD"
        text = _git(backend, "show", f"{rev}:{SPEC_IN_BACKEND}")
        origin = f"talki-backend {args.ref} ({_git(backend, 'rev-parse', '--short', rev).strip()})"

    if not text.lstrip().startswith("openapi:"):
        sys.exit(f"{origin} is not an OpenAPI document")
    if TARGET.exists() and TARGET.read_text(encoding="utf-8") == text:
        print(f"openapi/talki-v1.yaml already matches {origin}")
        return
    TARGET.write_bytes(text.encode())
    print(f"openapi/talki-v1.yaml updated from {origin}: now run `uv run scripts/generate.py`")


if __name__ == "__main__":
    main()
