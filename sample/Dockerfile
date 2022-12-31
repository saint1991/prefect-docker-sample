FROM prefecthq/prefect:2.7-python3.11 as runtime

COPY requirements.txt /requirements.txt

RUN apt-get update -y \
 && apt-get upgrade -y \
 && pip install -r /requirements.txt \
 && prefect block register -m prefect_docker

ENTRYPOINT ["prefect"]


FROM runtime as deployment

WORKDIR /workspace

COPY . /workspace
ENV PYTHONPATH=/workspace

ENTRYPOINT ["python", "deployment.py"]
