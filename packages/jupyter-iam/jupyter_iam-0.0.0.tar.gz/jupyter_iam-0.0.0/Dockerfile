# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

FROM python:3.11

RUN mkdir /opt/jupyter-iam

WORKDIR /opt/jupyter-iam

RUN pip install kazoo

COPY jupyter_iam /opt/jupyter_iam
RUN pip install -e ./jupyter_iam

# COPY frontplane/dist.html /opt/jupyter-iam/index.html

WORKDIR /opt/jupyter-iam/editor

EXPOSE 9300

CMD ["python", "-m", "jupyter_iam"]
