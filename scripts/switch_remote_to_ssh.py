#!/usr/bin/env python


import argparse
import subprocess
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("remote", nargs="?", default="origin")
args = parser.parse_args()

res = subprocess.run(["git", "remote", "get-url", args.remote], stdout=subprocess.PIPE)
url = res.stdout.decode().rstrip("\n")
parsed_url = urlparse(url)

if parsed_url.scheme.startswith("http"):
    ssh_url = f"git@{parsed_url.netloc}:{parsed_url.path.lstrip('/')}"
    print(f"Switching {args.remote} url from {url} to {ssh_url}")
    subprocess.run(["git", "remote", "set-url", args.remote, ssh_url])
