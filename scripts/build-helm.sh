#!/bin/sh

helm package -u charts/tfgrid-dashboard/
helm repo index --merge index.yaml .