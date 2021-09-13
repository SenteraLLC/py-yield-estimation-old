# Docker Image: https://github.com/lambgeo/docker-lambda
FROM lambgeo/lambda-gdal:3.3-python3.8

ENV PACKAGE_PREFIX=/var/task

# SSH config for Github authentication
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

#Install dependencies
COPY poetry.lock ${PACKAGE_PREFIX}/
COPY pyproject.toml ${PACKAGE_PREFIX}/
WORKDIR ${PACKAGE_PREFIX}/
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt -t .

# Create package.zip
RUN cd $PACKAGE_PREFIX && zip -r9q /tmp/package.zip *