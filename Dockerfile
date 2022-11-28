FROM python:3.8-slim AS builder
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME

ENV PYTHONUNBUFFERED=True
ENV PIP_NO_CACHE_DIR=True
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

# Install the python package managers.
RUN pip install -U \
    pip \
    setuptools \
    wheel \
    poetry
RUN groupadd -r dagster && useradd -m -r -g dagster dagster && \
    chown -R dagster:dagster $DAGSTER_HOME
# Set this folder at the system root and then cd into it.
WORKDIR $DAGSTER_HOME

# Copy poetry's package list and then install all non-developmental dependencies.
COPY . $DAGSTER_HOME

# Installs dependencies, but does *not* install our python code as a package because it's not mounted. Must be added afterward!

RUN poetry config virtualenvs.create false && poetry install -n --no-root --no-dev

# Setup a local instance of dagit and daemon
FROM builder AS dagit
EXPOSE 3000
RUN chown -R dagster:dagster $DAGSTER_HOME
USER dagster:dagster
CMD ["dagit", "-h", "0.0.0.0", "--port", "3000", "-w", "workspace.yaml"]

FROM builder AS daemon
USER dagster:dagster
CMD ["dagster-daemon", "run"]


