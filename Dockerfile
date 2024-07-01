ARG BUILD_IMAGE="artefact.skao.int/ska-cicd-k8s-tools-build-deploy:0.12.0"
ARG BASE_IMAGE="artefact.skao.int/ska-cicd-k8s-tools-build-deploy:0.12.0"


FROM $BUILD_IMAGE AS buildenv
FROM $BASE_IMAGE AS runtime

ENV APP_USER="oda"
ENV APP_DIR="/app"


ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL=${CAR_PYPI_REPOSITORY_URL}

# COPY --from=buildenv . .

USER root

RUN adduser $APP_USER --disabled-password --home $APP_DIR

WORKDIR /app

COPY --chown=$APP_USER:$APP_USER . .

RUN poetry config virtualenvs.create false
# Install runtime dependencies and the app
RUN poetry install --no-root

# Used by the FilesystemRepository implementation of the ODA
RUN mkdir -p /var/lib/oda && chown -R ${APP_USER} /var/lib/oda

# # Copy poetry.lock* in case it doesn't exist in the repo
# COPY pyproject.toml poetry.lock* ./

# # Install runtime dependencies and the app
# RUN poetry config virtualenvs.create false
# # Developers may want to add --dev to the poetry export for testing inside a container
# RUN poetry export --format requirements.txt --output poetry-requirements.txt --without-hashes && \
#     pip install -r poetry-requirements.txt && \
#     rm poetry-requirements.txt

USER ${APP_USER}

CMD ["python3", "-m", "ska_oso_pht_services.wsgi"]
