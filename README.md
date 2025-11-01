# GenAI-Incident-Triage-Engine
**AI Governance Triage Engine:** Uses **BigQuery ML** to instantly prioritize citizen incidents by urgency score. The **Cloud Run** API filters for critical issues (>0.45) and powers a real-time dashboard, enabling rapid, data-driven emergency response.

🇮🇳 Maharashtra Gov Decision Engine: AI-Driven Incident Triage

🌟 Unique Selling Proposition (USP)

The Governance Predictor: A secure, Google Cloud-native platform that instantly transforms Maharashtra's vast, siloed complaint data into predictive, actionable intelligence. We shift governance from reacting to complaints to proactively resolving high-risk service issues before they escalate, using BigQuery ML and real-time Cloud Run APIs.

🚀 Prototype & Working Features

The prototype is a real-time dashboard that visualizes the output of our Cloud Run Decision Engine API, demonstrating how departmental leaders can prioritize high-risk incidents instantly.

Prototype URL (Dashboard): [Insert your Cloud Storage Dashboard URL here]
API Endpoint (For Verification): [Insert your Cloud Run API URL here]

Working Features:

Real-Time ML Triage: The API fetches urgency scores and departmental predictions from a BigQuery ML model.

Instant Resource Analytics: The Bar Chart visualizes the volume of high-risk incidents per department.

Visualization & Prioritization: The Scatter Plot displays predicted risk scores for the top 20 incidents, allowing for immediate risk-based triage.

🛠️ Deployment Steps (GCP Cloud Shell)

This solution assumes you have deployed a BigQuery ML model (ML.PREDICT) and created a view/table containing the triaged results.

A. Prerequisites (Assumed Completed)

BigQuery ML model training is complete.

Service Account created with BigQuery Data Viewer and BigQuery Job User roles.

gcloud is authenticated and project is set to YOUR_PROJECT_ID.

B. Deploy the Cloud Run API (The Decision Engine)

Ensure all files (main.py, Dockerfile, requirements.txt) are in the current directory.

Build and Deploy the Cloud Run Service: This step will build the container and deploy the API, enabling the crucial CORS setting to allow the dashboard to fetch data.

gcloud run deploy decision-engine \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-cors=true


Note: This step directly addresses the "Failed to fetch" error by setting --set-cors=true.

C. Deploy the Dashboard (Static Website)

Define a unique bucket name:

PROJECT_ID=$(gcloud config get-value project)
DASHBOARD_BUCKET="maha-gov-dashboard-$PROJECT_ID"


Create the bucket (if it doesn't exist):

gsutil mb gs://$DASHBOARD_BUCKET


Upload the latestIndex.html dashboard file:

gsutil cp latestIndex.html gs://$DASHBOARD_BUCKET/


Make the files publicly readable for web access:

gsutil iam ch allUsers:objectViewer gs://$DASHBOARD_BUCKET


Configure the bucket for static website hosting:

gsutil web set -m latestIndex.html gs://$DASHBOARD_BUCKET


The final dashboard URL will be: https://storage.googleapis.com/$DASHBOARD_BUCKET/index.html
