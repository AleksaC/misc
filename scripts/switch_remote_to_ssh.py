#!/usr/bin/env python

# The script works for repos cloned from github using its https option
# It converts urls of the form https://github.com/owner/repo.git to git@github.com/owner/repo.git
# Needs to be tested for gitlab and bitbucket repos and also check what happens if 
# for instance .git is missing at the end

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
