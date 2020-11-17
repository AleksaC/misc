#!/usr/bin/env bash

set -eou pipefail

wd=$(pwd)

if [ ! -d $2 ];
then
    echo "Cannot find $2"
else
    cd $2;

    if [ ! -d $1 ];
    then
        echo "$1 needs to be relative to $2, not $wd"
        exit 1
    fi

    for f in $(ls -d $1/*);
    do
        dest="$(pwd)/$(basename $f)"
        echo "Linking $f to $dest"
        ln -s $f $dest
    done
fi
