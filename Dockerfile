FROM python:3.6
RUN pip install prometheus_client stellar-base
RUN mkdir -p /opt/stellar-horizon-exporter
COPY ./Dockerfile /opt/stellar-horizon-exporter/
COPY ./README.md /opt/stellar-horizon-exporter/
COPY ./stellar-horizon-exporter.py /opt/stellar-horizon-exporter/
WORKDIR /opt/stellar-horizon-exporter

ENTRYPOINT ["python3", "stellar-horizon-exporter.py"]
