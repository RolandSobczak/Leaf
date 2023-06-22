#!/bin/bash

set -o errexit
set -o nounset

celery \
    -A leaf.config.celery.celery \
    -b "${CELERY_BROKER_URL}" \
    flower \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
