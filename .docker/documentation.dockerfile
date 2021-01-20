ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION

ARG PYTHON_VERSION
RUN echo Using Python version $PYTHON_VERSION

# ADD ./ /sdk-python
# WORKDIR /sdk-python

# RUN pip install sphinx sphinxcontrib-apidoc sphinx_rtd_theme

# ENTRYPOINT [ "bash", "scripts/build_docs.sh"]

RUN pip install mkdocs
ADD mkdocs.yml /
ADD ./docs /docs
RUN ls -lash
RUN mkdocs build
WORKDIR /site
ENTRYPOINT ["python3", "-m", "http.server"]