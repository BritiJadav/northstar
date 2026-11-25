#!/usr/bin/env bash
# -------------------------------------------------------------
# NorthStar General Insurance - GCP Cloud Run Deployment Script
# -------------------------------------------------------------
set -e

PROJECT_ID="your-gcp-project-id" # Update with your GCP project ID
REGION="asia-south1"            # Mandatory India region (Mumbai) for DPDP compliance
SERVICE_NAME="northstar-intake-service"
REPO_NAME="northstar-repo"
IMAGE_TAG="v1.0.0"

echo "=== [1/4] Setting GCP Project and Region ==="
gcloud config set project ${PROJECT_ID}
gcloud config set run/region ${REGION}

echo "=== [2/4] Enabling Required Google Cloud APIs ==="
gcloud services enable \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com

echo "=== [3/4] Creating Artifact Registry Repository ==="
gcloud artifacts repositories create ${REPO_NAME} \
  --repository-format=docker \
  --location=${REGION} \
  --description="NorthStar Insurance Capstone Docker Repository" || true

echo "=== [4/4] Submitting Cloud Build and Deploying to Cloud Run ==="
gcloud builds submit --config=deploy/cloudbuild.yaml .

echo "=== Deployment Complete! Service URL: ==="
gcloud run services describe ${SERVICE_NAME} --format='value(status.url)'
