ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION

ARG PYTHON_VERSION
RUN echo Using Python version $PYTHON_VERSION

RUN pip install --upgrade pip
RUN pip install pytest pytest-pylint

ADD ./ /sdk-python
WORKDIR /sdk-python
RUN rm setup.cfg

RUN pip install -e .

ENTRYPOINT [ "pytest", "--pylint", "-m", "pylint", "./UKFastAPI"]
