#!/usr/bin/env bash
set -e

# Build project in amazonlinux Docker image for deployment on AWS Lambda
BASEDIR=$(git rev-parse --show-toplevel)
docker build ${BASEDIR} \
       --tag yield-estimation
       #--build-arg SSH_PRIVATE_KEY="${SSH_PRIVATE_KEY}"

# Remove previous results
rm -rf ${BASEDIR}/dist || true

# Copy dist.zip from Docker image
#VERSION="v$(cat ${BASEDIR}/.version)-$(date +'%Y%m%d-%H%M%S')"
VERSION=$(wget -O - https://github.com/SenteraLLC/version.sh/raw/master/version.sh | bash)
mkdir -p ${BASEDIR}/dist/$(dirname ${VERSION})
docker run \
       --volume ${BASEDIR}:/local \
       --rm -it \
       yield-estimation \
       cp /tmp/package.zip /local/dist/${VERSION}.zip