FROM quay.io/modh/odh-trustyai-notebook@sha256:8c5e653f6bc6a2050565cf92f397991fbec952dc05cdfea74b65b8fd3047c9d4
LABEL authors="hjrnunes"

USER 1001

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt