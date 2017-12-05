#!/bin/bash
# this script uses the CONDA_UPLOAD_TOKEN env var

# To return a failure if any commands inside fail
set -e

echo "Deploying to Anaconda.org..."
anaconda upload $HOME/miniconda/conda-bld/noarch/pywerami-*.tar.bz2 -t $CONDA_UPLOAD_TOKEN --force
echo "Successfully deployed to Anaconda.org."

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e
