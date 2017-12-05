#!/bin/bash
# this script uses the CONDA_UPLOAD_TOKEN env var

# To return a failure if any commands inside fail
set -e

echo "Deploying to Anaconda.org..."
anaconda -t $CONDA_UPLOAD_TOKEN upload -u ondrolexa ~/conda-bld/**/apsg-*.tar.bz2 --force
echo "Successfully deployed to Anaconda.org."

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e
