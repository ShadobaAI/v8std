"""Read-only upstream comparison and protected-corpus verification."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PROTECTED = ("docs/corporate", "docs/yaxunit", "docs/vanessa")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="upstream/main", help="Already fetched upstream ref.")
    parser.add_argument("--verify-protected", metavar="BASE", help="Fail if protected trees differ from BASE, including uncommitted tracked changes.")
    args = parser.parse_args(argv)
    if args.verify_protected:
        changed = git("diff", "--name-only", args.verify_protected, "--", *PROTECTED)
        untracked = git("ls-files", "--others", "--exclude-standard", "--", *PROTECTED)
        if changed or untracked:
            print("Protected corpus changed:\n" + "\n".join(filter(None, (changed, untracked))))
            return 1
        print("Protected corpus unchanged: corporate, yaxunit, vanessa")
        return 0
    base = git("merge-base", "HEAD", args.ref)
    behind = git("rev-list", "--count", f"HEAD..{args.ref}")
    ahead = git("rev-list", "--count", f"{args.ref}..HEAD")
    upstream = set(git("diff", "--name-only", f"{base}..{args.ref}").splitlines())
    fork = set(git("diff", "--name-only", f"{base}..HEAD").splitlines())
    print(f"Upstream: {args.ref} ({git('rev-parse', '--short', args.ref)})")
    print(f"Merge base: {base}; incoming commits: {behind}; fork commits: {ahead}")
    for title, paths in (("Incoming paths", upstream), ("Changed on both sides (review before merge)", upstream & fork)):
        print(f"\n{title}: {len(paths)}")
        for path in sorted(paths):
            print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
