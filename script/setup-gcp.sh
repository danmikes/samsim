#!/bin/bash
PROJECT_ID="your-project-id-here"

# Enable APIs
gcloud services enable iamcredentials.googleapis.com run.googleapis.com artifactregistry.googleapis.com

# Create service account
gcloud iam service-accounts create "github-actions" \
  --display-name="GitHub Actions Service Account"

# Grant roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

echo "PROJECT_ID: $PROJECT_ID"
echo "Service Account: github-actions@$PROJECT_ID.iam.gserviceaccount.com"
