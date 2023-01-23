# Dagster libraries to run both dagit and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.10.9-slim

COPY ["./requirements_ui.txt", "."] 
RUN pip3 install -r requirements_ui.txt

# Set $DAGSTER_HOME and copy dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml workspace.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME