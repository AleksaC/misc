#!/usr/bin/env bash

set -eou pipefail

GH_USER=$1
GH_REPO=$2

ssh-keygen -m pem -b 4096 -N '' -f ./id_rsa

curl \
    -X POST \
    -H "Accept: application/vnd.github.v3+json" \
    -H "Authorization: token $GH_TOKEN" \
    "https://api.github.com/repos/$GH_USER/$GH_REPO/keys" \
    -d "{\"key\":\"$(cat id_rsa.pub)\", \"title\": \"CircleCI push\"}"

curl \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Circle-Token: $CIRCLE_TOKEN" \
    "https://circleci.com/api/v1.1/project/github/$GH_USER/$GH_REPO/ssh-key" \
    -d "{\"hostname\":\"github.com\",\"private_key\":\"$(cat id_rsa)\"}"
