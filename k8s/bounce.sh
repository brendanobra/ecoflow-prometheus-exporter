#!/bin/sh
kubectl create ns solar 
kubectl -n solar delete -f deployment.yaml
kubectl -n solar apply -f deployment.yaml
