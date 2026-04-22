FROM python:3.13-slim-bookworm as build

ARG USER_NAME="swc"
ARG VENVS_PATH="/srv/virtualenvs"

ARG DEVELOPMENT=0

RUN apt-get update \
    && apt-get -y -m --no-install-recommends install \
      build-essential \
      libpq-dev \
      libssl-dev \
    && apt-get clean

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml "${VENVS_PATH}/pyproject.toml"
COPY uv.lock "${VENVS_PATH}/uv.lock"

WORKDIR "$VENVS_PATH"

RUN if [ "$DEVELOPMENT" = 1 ]; then \
       uv sync --group dev --locked --no-editable; else \
       uv sync --no-group dev --locked --no-editable; fi


FROM python:3.13-slim-bookworm AS final

ARG USER_NAME="swc"
ARG APP_CODE="/srv/applications/${USER_NAME}"

RUN groupadd -g 1000 "${USER_NAME}" \
    && useradd -u 1000 -g "${USER_NAME}" -s /bin/bash -d "/srv" "${USER_NAME}"

ENV PYTHONUNBUFFERED 1
ARG VENVS_PATH="/srv/virtualenvs"
ARG APP_VENV="${VENVS_PATH}/.venv"
ENV PATH="${APP_VENV}/bin:${PATH}"


RUN apt-get update

RUN apt install -y postgresql-common
RUN /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y
RUN apt install -y postgresql-client-18

RUN apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown="${USER_NAME}:${USER_NAME}" --from=build "${APP_VENV}" "${APP_VENV}"
COPY --chown="${USER_NAME}:${USER_NAME}" src/ "${APP_CODE}/"

RUN chown "${USER_NAME}:${USER_NAME}" "/srv" "/run"

USER "${USER_NAME}"
WORKDIR "${APP_CODE}"
VOLUME "${APP_CODE}"
