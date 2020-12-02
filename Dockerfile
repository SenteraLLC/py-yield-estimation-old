# Docker Image: https://github.com/lambgeo/docker-lambda
FROM lambgeo/lambda-gdal:3.2-python3.8

ENV PACKAGE_PREFIX=/var/task

# SSH config for Github authentication
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

################################################################################
#                            INSTALL DEPENDENCIES                              #
################################################################################

# Install non-scientific (i.e. no numpy/scipy) dependencies: -------------------
RUN pip install geojson sat-search intake-stac -t ${PACKAGE_PREFIX}/ -U
RUN pip install lambda-proxy -t ${PACKAGE_PREFIX}/ -U

# Install dependencies of scientific dependencies: -----------------
RUN pip install affine attrs click cligj enum34 click-plugins -t ${PACKAGE_PREFIX}/ -U

# Install scientific dependencies, using 'no-deps' to force numpy/scipy to not install:
RUN pip install --no-deps rasterio --no-binary :all: -t ${PACKAGE_PREFIX}/ -U
RUN pip install --no-deps rio-tiler==2.0.0rc1 -t ${PACKAGE_PREFIX}/ -U

# Reduce size of the C libs and strip .py files
RUN cd $PREFIX && find lib -name \*.so\* -exec strip {} \;
RUN find $PACKAGE_PREFIX -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-38//'); cp $f $n; done;
RUN find $PACKAGE_PREFIX -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN find $PACKAGE_PREFIX -type f -a -name '*.py' -print0 | xargs -0 rm -f
RUN du -sh $PACKAGE_PREFIX

################################################################################
#                              CREATE ARCHIVE                                  #
################################################################################
COPY src/handler.py ${PACKAGE_PREFIX}/handler.py
COPY src ${PACKAGE_PREFIX}/src

# Create package.zip
RUN cd $PACKAGE_PREFIX && zip -r9q /tmp/package.zip *
RUN cd $PREFIX && zip -r9q --symlinks /tmp/package.zip lib/*.so* share
RUN cd $PREFIX && zip -r9q --symlinks /tmp/package.zip bin/gdal* bin/ogr* bin/geos* bin/nearblack