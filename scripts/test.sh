#!/usr/bin/env bash

set -e
set -x

poetry run python -m coverage run -m pytest -lv ${ARGS}
poetry run python -m coverage report -m
