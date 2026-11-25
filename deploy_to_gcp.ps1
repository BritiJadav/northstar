# ==============================================================================
# NorthStar General Insurance - Automated Google Cloud Run Global Deployment
# Region: asia-south1 (Mumbai - India DPDP Act 2023 Compliant)
# ==============================================================================

$ErrorActionPreference = "Continue"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " NORTHSTAR GENERAL INSURANCE - GCP CLOUD RUN DEPLOYMENT " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# 1. Configure Cloud SDK Python Environment
$env:CLOUDSDK_PYTHON = "C:\Python315\python.exe"
$GCLOUD_CMD = "C:\ProgramData\chocolatey\lib\gcloudsdk\tools\google-cloud-sdk\bin\gcloud.cmd"

if (-not (Test-Path $GCLOUD_CMD)) {
    $GCLOUD_CMD = "gcloud"
}

# 2. Project & Region Configuration
$REGION = "asia-south1"
$PROJECT = "slabspro-slabsuser41"
$SERVICE_NAME = "northstar-intake-service"
$IMAGE_TAG = "asia-south1-docker.pkg.dev/$PROJECT/cloud-run-source-deploy/$SERVICE_NAME`:v1"
$STAGING_DIR = "gs://$PROJECT-source-staging/source"
$BUILD_SA = "projects/$PROJECT/serviceAccounts/slabsuser41-service-account@$PROJECT.iam.gserviceaccount.com"
$RUN_SA = "slabsuser41-service-account@$PROJECT.iam.gserviceaccount.com"

Write-Host "[1/4] Active Project: $PROJECT in Region: $REGION" -ForegroundColor Yellow

# 3. Cloud Build Container Build & Push
Write-Host "`n[2/4] Packaging & Building Container via Google Cloud Build..." -ForegroundColor Yellow
& $GCLOUD_CMD builds submit `
    --config=cloudbuild.yaml `
    --region=$REGION `
    --gcs-source-staging-dir=$STAGING_DIR `
    --service-account=$BUILD_SA `
    --project=$PROJECT

# 4. Deploy Container to Cloud Run
Write-Host "`n[3/4] Deploying Service to Google Cloud Run..." -ForegroundColor Yellow
& $GCLOUD_CMD run deploy $SERVICE_NAME `
    --image=$IMAGE_TAG `
    --region=$REGION `
    --platform=managed `
    --port=8080 `
    --service-account=$RUN_SA `
    --project=$PROJECT `
    --quiet

# 5. Retrieve Live URL
Write-Host "`n[4/4] Verifying Cloud Run Service Status..." -ForegroundColor Yellow
$SERVICE_URL = & $GCLOUD_CMD run services describe $SERVICE_NAME --region $REGION --project $PROJECT --format="value(status.url)"

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " ✔ CLOUD RUN SERVICE IS LIVE ON GOOGLE CLOUD!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host "Global Service URL:         $SERVICE_URL" -ForegroundColor Cyan
Write-Host "Workbench Cockpit:          $SERVICE_URL/" -ForegroundColor Cyan
Write-Host "10-Slide Presentation Deck: $SERVICE_URL/slides" -ForegroundColor Cyan
Write-Host "Interactive Swagger API:    $SERVICE_URL/docs" -ForegroundColor Cyan
Write-Host "Health & Governance Probe:  $SERVICE_URL/health`n" -ForegroundColor Cyan
