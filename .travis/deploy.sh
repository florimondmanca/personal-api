#!/bin/bash
git stash --all
git fetch --unshallow
git checkout master
git push --force dokku master
