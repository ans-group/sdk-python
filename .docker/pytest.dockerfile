ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION

ARG PYTHON_VERSION
RUN echo Using Python version $PYTHON_VERSION

RUN pip install --upgrade pip
RUN pip install vcrpy

# Installs the appropriate pytest version based on the Python image.
# Also install pytest-cov if Python 3.4+.
RUN if [ "$(echo $PYTHON_VERSION | cut -d'.' -f 1)" -eq 3 ] && [ "$(echo $PYTHON_VERSION | cut -d'.' -f 2)" -lt 5 ] ; then echo "Installing older pytest version..." && pip install "pytest<5" ; else echo "Installing latest pytest version..." && pip install pytest pytest-cov; fi

ADD ./ /actions_test
WORKDIR /actions_test
RUN mkdir -p reports 

RUN pip install -e .
# RUN if [ "$(echo $PYTHON_VERSION | cut -d'.' -f 1)" -eq 3 ] && [ "$(echo $PYTHON_VERSION | cut -d'.' -f 2)" -lt 5 ] ; then echo "" ; else echo "" && rm setup.cfg && mv setup_ci.cfg setup.cfg; fi

# RUN ls -lash
ENTRYPOINT [ "pytest", "-vs"]
