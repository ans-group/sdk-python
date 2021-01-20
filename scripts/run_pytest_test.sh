docker run -it --env-file=../.env --mount type=bind,source="$(pwd)"/../reports,target=/sdk-python/reports $(docker build -q -f ../.docker/pytest.dockerfile ..)
