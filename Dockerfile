FROM remotepixel/amazonlinux:gdal3.0-py3.7

ENV PACKAGE_PREFIX=/var/task

################################################################################
#                            INSTALL DEPENDENCIES                              #
################################################################################

# Install non-scientific (i.e. no numpy/scipy) dependencies: -------------------
RUN pip3 install geojson sat-search intake-stac -t ${PACKAGE_PREFIX}/ -U
RUN pip3 install lambda-proxy -t ${PACKAGE_PREFIX}/ -U

# Install dependencies of scientific dependencies TODO...: -----------------
RUN pip3 install affine attrs click cligj joblib pyparsing click-plugins -t ${PACKAGE_PREFIX}/ -U

# Install scientific dependencies, using 'no-deps' to force numpy/scipy to not install:
RUN pip3 install --no-deps rasterio --no-binary :all: -t ${PACKAGE_PREFIX}/ -U
RUN pip3 install --no-deps rio-tiler==2.0.0rc1 -t ${PACKAGE_PREFIX}/ -U


################################################################################
#                              CREATE ARCHIVE                                  #
################################################################################
COPY src/handler.py ${PACKAGE_PREFIX}/handler.py
COPY src ${PACKAGE_PREFIX}/src

RUN cd $PACKAGE_PREFIX && zip -r9q /tmp/package.zip *
RUN cd $PREFIX && zip -r9q --symlinks /tmp/package.zip lib/*.so* share
RUN cd $PREFIX && zip -r9q --symlinks /tmp/package.zip bin/gdal* bin/ogr* bin/geos* bin/nearblack