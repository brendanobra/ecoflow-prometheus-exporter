# ecoflow-prometheus-exporter
A Simple Ecoflow JSON REST API -> prometheus metrics converter
##
Disclaimer: This project is in no way connected to Ecoflow the company, and is entirely developed as a fun project (with no guarantees of anything)
##
A very simple implementation of a prometheus exporter for Ecoflow (https://https://www.ecoflow.com/) products that support the EcoFlow IOT backend.

I wanted to monitor and alert (not on a mobile app) on the status of my Delta Pro , and could not find any existing solutions.  This project is what I came up with...

The project provides:
- a DEAD simple python program that accepts a number of arguments to collect information about an ecoflow product and then exports the collected information to 
a prometheus endpoint
- a docker image (https://hub.docker.com/repository/docker/brendanobra/ecoflow-prometheus-exporter) for convenience 

All metrics produced are prefixed with `ecoflow` , for instance `ecoflow_watts_out`
While this was developed to run on premises in a small kubernetes cluster, with the end goal of visualizing the data in grafana, the exporter/docker image are not
dependent on grafana.
####
Usage
1) get your unit's serial number (displayed on inside of IOT port cover)
2) email support@ecoflow.com with the serial number and request IOT REST api access
3) Support will respond with an app key and secret key. save them (and don't share with anyone)
4) clone this repo (or `docker run` the image). 
5) The program is parameterized via environment variables:
required:

`DEVICE_SN` - the device serial number

`APP_KEY` - the app key provided by support

`SECRET_KEY` - the secret key provided by support

optional:

`ARRAY_CAPACITY` - the nominal production capacity of the charging source in watts (for example 1000 for a 1000 watt solar array)

`POLLING_INTERVAL_SECONDS` - the interval to poll the Ecoflow APIs

example of running docker image: 

`docker run -e DEVICE_SN=<your device SN> -e APP_KEY=<your app key provided by support> -e SECRET_KEY=<your secret key provided by support> -it -p 9090:9090 --network=host brendanobra/ecoflow-prometheus-exporter`

will run the image with the exporter running on <your computers ip address>:9090

Example dashboard (dashboard source not currently included, but shows what can be made with the data):
![](ecoflow_dash.png?raw=true)
