ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION

ARG PYTHON_VERSION
RUN echo Using Python version $PYTHON_VERSION

ADD ./ /sdk-python
WORKDIR /sdk-python

ENTRYPOINT [ "python", "setup.py", "sdist"]