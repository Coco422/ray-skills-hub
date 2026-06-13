#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_REPO = "Coco422/ray-skills-hub"
DEFAULT_REF = "main"
DEFAULT_TIMEOUT = 30


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
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Network timeout in seconds.")
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def safe_repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        fail("--path must be a relative path inside the repo")
    return path


def request(url: str, timeout: int):
    headers = {"User-Agent": "ray-skills-hub-installer"}
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout)


def fetch_json(url: str, timeout: int) -> dict:
    try:
        with request(url, timeout) as response:
            return json.load(response)
    except Exception as exc:
        fail(f"failed to fetch {url}: {exc}")


def fetch_bytes(url: str, timeout: int) -> bytes:
    try:
        with request(url, timeout) as response:
            return response.read()
    except Exception as exc:
        fail(f"failed to download {url}: {exc}")


def list_skill_files(repo: str, ref: str, skill_path: Path, timeout: int) -> list[tuple[str, Path]]:
    encoded_ref = urllib.parse.quote(ref, safe="")
    url = f"https://api.github.com/repos/{repo}/git/trees/{encoded_ref}?recursive=1"
    tree = fetch_json(url, timeout).get("tree", [])
    prefix = skill_path.as_posix().strip("/") + "/"
    files: list[tuple[str, Path]] = []

    for item in tree:
        source_path = item.get("path", "")
        if item.get("type") != "blob" or not source_path.startswith(prefix):
            continue
        relative = Path(source_path[len(prefix) :])
        if not relative.parts or ".." in relative.parts:
            fail(f"unsafe file path in GitHub tree: {source_path}")
        files.append((source_path, relative))

    if not any(relative.as_posix() == "SKILL.md" for _, relative in files):
        fail(f"{skill_path} does not contain SKILL.md")
    return files


def raw_url(repo: str, ref: str, source_path: str) -> str:
    encoded_ref = urllib.parse.quote(ref, safe="")
    encoded_path = urllib.parse.quote(source_path, safe="/")
    return f"https://raw.githubusercontent.com/{repo}/{encoded_ref}/{encoded_path}"


def install_skill(args: argparse.Namespace, repo_path: Path, name: str) -> Path:
    files = list_skill_files(args.repo, args.ref, repo_path, args.timeout)
    dest_root = Path(args.dest).expanduser()
    target = dest_root / name
    dest_root.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not args.force:
            fail(f"{target} already exists; pass --force to replace it")

    with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=dest_root) as tmp:
        staged = Path(tmp) / name
        for source_path, relative in files:
            destination = staged / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(fetch_bytes(raw_url(args.repo, args.ref, source_path), args.timeout))
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staged), target)

    return target


def main() -> None:
    args = parse_args()
    repo_path = safe_repo_path(args.path)
    install_name = args.name or repo_path.name

    installed = install_skill(args, repo_path, install_name)
    print(f"Installed {install_name} to {installed}")


if __name__ == "__main__":
    main()
