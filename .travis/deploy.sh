#!/bin/bash
git stash --all
git checkout master
git push --force dokku master
