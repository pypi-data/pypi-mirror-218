# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

FROM python:3.11

RUN mkdir /opt/jupyter-operator

WORKDIR /opt/jupyter-operator

RUN pip install kazoo

COPY jupyter_operator /opt/jupyter_operator
RUN pip install -e ./jupyter_operator

# COPY frontplane/dist.html /opt/jupyter-operator/index.html

WORKDIR /opt/jupyter-operator/editor

EXPOSE 9300

CMD ["python", "-m", "jupyter_operator"]
