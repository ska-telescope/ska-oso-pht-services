ARG BUILD_IMAGE="artefact.skao.int/ska-cicd-k8s-tools-build-deploy:0.12.0"
ARG BASE_IMAGE="artefact.skao.int/ska-cicd-k8s-tools-build-deploy:0.12.0"


FROM $BUILD_IMAGE AS buildenv
FROM $BASE_IMAGE AS runtime

ENV APP_USER="oda"
ENV APP_DIR="/app"


ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL=${CAR_PYPI_REPOSITORY_URL}

USER root

RUN adduser $APP_USER --disabled-password --home $APP_DIR

WORKDIR /app

COPY --chown=$APP_USER:$APP_USER . .

RUN poetry config virtualenvs.create false
# Install runtime dependencies and the app
RUN poetry install --no-root

# Used by the FilesystemRepository implementation of the ODA
RUN mkdir -p /var/lib/oda && chown -R ${APP_USER} /var/lib/oda

USER ${APP_USER}

CMD ["python3", "-m", "ska_oso_pht_services.wsgi"]
