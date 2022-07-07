#!/bin/sh
kubectl create ns solar 
kubectl -n solar apply -f deployment.yaml
