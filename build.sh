#!/bin/sh
docker build -t ecoflow_exporter -t docker-registry.home:80/ecoflow_exporter -t brendanobra/ecoflow-prometheus-exporter:latest .
docker push  docker-registry.home:80/ecoflow_exporter
docker push brendanobra/ecoflow-prometheus-exporter:latest
