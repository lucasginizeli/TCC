FROM amazonlinux:2.0.20210219.0 AS build-stage

RUN yum upgrade -y
RUN yum install -y gcc gcc-c++ make freetype-devel yum-utils findutils openssl-devel git zip

ARG PYTHON_VERSION_WITH_DOT=3.8
ARG PYTHON_VERSION_WITHOUT_DOT=38

RUN amazon-linux-extras install -y python${PYTHON_VERSION_WITH_DOT} && \
        yum install -y python${PYTHON_VERSION_WITHOUT_DOT}-devel

ARG INSTBASE=/var/task

WORKDIR ${INSTBASE}
RUN python${PYTHON_VERSION_WITH_DOT} -m venv venv

COPY requirements.txt lambda_function.py ./

RUN venv/bin/pip install \
        -r requirements.txt \
        psycopg2-binary \
        apig-wsgi

# Create lambda_venv_path.py
RUN INSTBASE=${INSTBASE} venv/bin/python -c \
    'import os; import sys; instbase = os.environ["INSTBASE"]; print("import sys; sys.path[:0] = %s" % [p for p in sys.path if p.startswith(instbase)])' \
    > ${INSTBASE}/lambda_venv_path.py

COPY empresas empresas
COPY TCC TCC
COPY static static

# Remove artifacts that won't be used.
# If lib64 is a symlink, remove it.
RUN rm -rf venv/bin venv/share venv/include && \
        (if test -h venv/lib64 ; then rm -f venv/lib64 ; fi)

RUN zip -r9q /tmp/lambda.zip *

# Generate a filesystem image with just the zip file as the output.
# See: https://docs.docker.com/engine/reference/commandline/build/#custom-build-outputs
FROM scratch AS export-stage
COPY --from=build-stage /tmp/lambda.zip /