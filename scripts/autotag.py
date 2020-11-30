#!/usr/bin/env python

import argparse
import re
import subprocess
import sys
import textwrap

from typing import NamedTuple
from typing import Optional
from typing import Sequence

PRETTY_FORMAT = "[%H] %D"
VERSION_RE = re.compile(
    r"(\[[0-9a-f]{5,40}\]).*tag: (v?([0-9])+\.([0-9])+\.([0-9]+)).*\n"
)


class Version(NamedTuple):
    major: int
    minor: int
    patch: int
    string: str  # This attribute is needed because both vx.y.z and x.y.z tags are supported

    def __repr__(self):
        return self.string

    def __lte__(self, other: "Version") -> bool:
        if self.major < other.major or self.major > other.major:
            return self.major < other.major
        elif self.minor < other.minor or self.minor > other.minor:
            return self.minor < other.minor
        else:
            return self.patch <= other.patch


def print_stderr(stderr: bytes) -> None:
    print(f"Something went wrong:\n\n{textwrap.indent(stderr.decode(), ' ' * 4)}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    versions = ["--major", "--minor", "--patch"]
    parser = argparse.ArgumentParser()
    parser.add_argument("rev", nargs="?", default="HEAD", help="Revision to tag")
    parser.add_argument(
        "version",
        nargs="?",
        choices=versions,
        default="--patch",
        help="Version to increment. Defaults to --patch",
    )

    known, unknown = parser.parse_known_args(argv)

    if len(unknown) == 1 and unknown[0] in versions:
        known.version = unknown[0]
    else:
        for arg in unknown.copy():
            if arg in versions:
                unknown.remove(arg)
                parser.error(f"unrecognized arguments: {' '.join(unknown)}")

    return known


def get_latest_version(rev: str = "HEAD") -> Optional[Version]:
    res = subprocess.run(
        ["git", "log", f"--pretty=format:{PRETTY_FORMAT}", rev],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if res.returncode != 0:
        print_stderr(res.stderr)
        return None

    revs = res.stdout.decode().strip() + "\n"

    latest_version = re.search(VERSION_RE, revs)
    if latest_version is None:
        return Version(0, 0, 0, "v0.0.0")
    latest_sha, version, *version_numbers = latest_version.groups()

    res = subprocess.run(["git", "rev-parse", rev], stdout=subprocess.PIPE)
    sha = res.stdout.decode().strip()
    if sha == latest_sha[1:-1]:
        print(f"{rev} is already tagged by {version}")
        return None

    major, minor, patch = map(int, version_numbers)

    return Version(major, minor, patch, version)


def get_next_version(rev: str = "HEAD") -> Optional[Version]:
    res = subprocess.run(
        ["git", "log", f"--pretty=format:{PRETTY_FORMAT}", f"{rev}.."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if res.returncode != 0:
        print_stderr(res.stderr)
        return None

    revs = res.stdout.decode().strip() + "\n"

    next_version = re.search(VERSION_RE, revs)
    if next_version is None:
        return None
    else:
        _, version, *version_numbers = next_version.groups()
        major, minor, patch = map(int, version_numbers)
        return Version(major, minor, patch, version)


def increment_version(version: Version, increment: str) -> Version:
    major, minor, patch, version_string = version
    if increment == "--major":
        major += 1
        minor = 0
        patch = 0
    elif increment == "--minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    if version_string.startswith("v"):
        version_string = f"v{major}.{minor}.{patch}"

    return Version(major, minor, patch, version_string)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    current_version = get_latest_version(args.rev)
    if current_version is None:
        return 1

    new_version = increment_version(current_version, args.version)

    next_version = get_next_version(args.rev)
    if next_version is not None and next_version <= new_version:
        print(
            f"Cannot tag {args.rev} with version {new_version}, there already exists "
            f"a tag with version superseding it - {next_version}"
        )
        return 1

    print(f"Adding {new_version} tag to {args.rev}")
    res = subprocess.run(["git", "tag", new_version.string, args.rev])

    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
