# stellar-horizon-exporter

A prometheus exporter for <https://horizon.stellar.org/>. Provides Prometheus metrics from the all operation API endpoint of Stellar Horizon, such as Number of operations, Number of payments, Sum of payments, Number of account creations, etc. [REST API Documentation found here](https://www.stellar.org/developers/horizon/reference/endpoints/operations-all.html).

When running this exporter with both Prometheus and Grafana, [you can create dashboards like](https://grafana.com/dashboards/6429):

![stellar-horizon-dashboard](https://github.com/smorano/stellar-horizon-exporter/raw/master/img/stellar-horizon-dashboard.png "stellar-horizon-exporter with Prometheus and Grafana")

# Developing

- Build the image:

```
docker build -t stellar-horizon-exporter .
```

- Run it while listening on localhost:9100:

```
docker run --rm -p 127.0.0.1:9101:9101 stellar-horizon-exporter
```

- Run it interactively:

```
docker run --rm -it --entrypoint=/bin/bash -p 127.0.0.1:9101:9101 -v ${PWD}:/opt/stellar-horizon-exporter stellar-horizon-exporter
```

- Then to launch:

```
python stellar-horizon-exporter.py
```

# Testing the Prometheus Grafana Stack

- In the `prometheus-compose` directory, run:

```
docker-compose up
```

- Go to <http://localhost:3000>.  Log in as `admin/admin`. 
- To import the dashboard, click the "Home" button at the top, then on the right, click "Import Dashboard".
- Enter `6429` in the "Grafana.com Dashboard" field.
- Select the "prometheus" data source.
- Modify the other settings as preferred. Click "Import".
- The new dashboard should be selectable and found at <http://localhost:3000/dashboard/db/stellar-horizon-dashboard>.
- The Prometheus interface can be accessed at <http://localhost:9090>

# Thanks and Links

- Stellar horizon API link - <https://www.stellar.org/developers/horizon/reference/>
- Prometheus exporters - <https://prometheus.io/docs/instrumenting/writing_exporters/>
- Prometheus Python Client - <https://github.com/prometheus/client_python>
- Grafana Dashboard - <https://grafana.com/dashboards/6429>

