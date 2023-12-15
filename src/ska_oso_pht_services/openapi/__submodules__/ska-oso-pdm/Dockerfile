ARG BUILD_IMAGE="artefact.skao.int/ska-tango-images-pytango-builder:9.3.32"
ARG BASE_IMAGE="artefact.skao.int/ska-tango-images-pytango-runtime:9.3.19"

FROM $BUILD_IMAGE AS buildenv
FROM $BASE_IMAGE AS runtime

ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL=${CAR_PYPI_REPOSITORY_URL}

USER root

# Copy poetry.lock* in case it doesn't exist in the repo
WORKDIR /app

# Install runtime dependencies and the app
COPY pyproject.toml poetry.lock* ./

# Developers may want to add --dev to the poetry export for testing inside a container
RUN poetry export --format requirements.txt --output poetry-requirements.txt --without-hashes && \
    pip install -r poetry-requirements.txt && \
    rm poetry-requirements.txt

USER tango

# Install runtime dependencies and the app
RUN poetry config virtualenvs.create false


CMD ["python3"]
