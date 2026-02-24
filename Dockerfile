FROM quay.io/modh/odh-trustyai-notebook:v3-20250827-3a59e5e
LABEL authors="hjrnunes"

USER 1001

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt