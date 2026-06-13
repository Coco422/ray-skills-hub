#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_REPO = "Coco422/ray-skills-hub"
DEFAULT_REF = "main"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install one skill folder from a GitHub repo.")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo in owner/name form.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="Branch, tag, or commit to install from.")
    parser.add_argument("--path", required=True, help="Skill directory path inside the repo.")
    parser.add_argument(
        "--dest",
        default=os.environ.get("CODEX_HOME", str(Path.home() / ".codex")) + "/skills",
        help="Destination skills directory.",
    )
    parser.add_argument("--name", help="Installed directory name. Defaults to source folder name.")
    parser.add_argument("--force", action="store_true", help="Replace an existing skill directory.")
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def safe_repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        fail("--path must be a relative path inside the repo")
    return path


def download_archive(repo: str, ref: str, target: Path) -> None:
    url = f"https://codeload.github.com/{repo}/zip/{ref}"
    try:
        urllib.request.urlretrieve(url, target)
    except Exception as exc:
        fail(f"failed to download {url}: {exc}")


def unpack_archive(archive: Path, target: Path) -> Path:
    try:
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extractall(target)
    except zipfile.BadZipFile:
        fail("downloaded archive is not a valid zip file")

    roots = [item for item in target.iterdir() if item.is_dir()]
    if len(roots) != 1:
        fail("unexpected GitHub archive layout")
    return roots[0]


def install_skill(source: Path, dest_root: Path, name: str, force: bool) -> Path:
    if not (source / "SKILL.md").is_file():
        fail(f"{source} does not contain SKILL.md")

    target = dest_root / name
    dest_root.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not force:
            fail(f"{target} already exists; pass --force to replace it")
        shutil.rmtree(target)

    shutil.copytree(source, target)
    return target


def main() -> None:
    args = parse_args()
    repo_path = safe_repo_path(args.path)
    install_name = args.name or repo_path.name

    with tempfile.TemporaryDirectory(prefix="ray-skills-hub-") as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / "repo.zip"
        download_archive(args.repo, args.ref, archive)
        archive_root = unpack_archive(archive, tmp_path / "repo")
        installed = install_skill(archive_root / repo_path, Path(args.dest).expanduser(), install_name, args.force)

    print(f"Installed {install_name} to {installed}")


if __name__ == "__main__":
    main()
