"""Fail a tagged package build when its tag and project version disagree."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "pyproject.toml").open("rb") as source:
        version = tomllib.load(source)["project"]["version"]
    tag = os.environ.get("GITHUB_REF_NAME", "")
    ref_type = os.environ.get("GITHUB_REF_TYPE", "")
    if ref_type == "tag" and tag != f"v{version}":
        raise SystemExit(f"Release tag {tag!r} does not match project version v{version}")
    print(f"Release version verified: {version}")


if __name__ == "__main__":
    main()
