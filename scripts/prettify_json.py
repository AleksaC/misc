#!/bin/env python

import argparse
import json
import os
from glob import glob

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i", "--indent", type=int, default=4, help="Indent size in the prettified output"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="When set the prettified json is only printed to stdout",
)
parser.add_argument(
    "filenames",
    nargs="+",
    help="Names of the json files to be prettified (wildcards are supported)",
)

args = parser.parse_args()

for pattern in args.filenames:
    filenames = glob(pattern)

    if not filenames:
        print(f"{os.path.abspath(pattern)} does not exist")

    for filename in glob(pattern):
        with open(filename, "r+") as f:
            try:
                content = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f"{filename} does not contain valid json!")
                continue

            prettified = json.dumps(content, indent=args.indent)

            if args.dry_run:
                print(prettified)
            else:
                f.seek(0)
                f.write(prettified)
                f.truncate()
