# Customer Segmentation API

FastAPI backend serving customer segmentation analysis results for the Customer Segmentation case study.

## Overview
REST API that serves pre-computed RFM analysis and K-Means clustering results as JSON endpoints, consumed by the React frontend dashboard.

## Endpoints
- `GET /` — Health check
- `GET /api/cleaning-summary` — Data cleaning decisions and row counts
- `GET /api/country-distribution` — Top 10 countries by customer count
- `GET /api/monthly-revenue` — Monthly revenue over time
- `GET /api/revenue-distribution` — Customer revenue distribution
- `GET /api/cumulative-revenue` — Lorenz curve data
- `GET /api/segment-summary` — Four segment profiles with average RFM values
- `GET /api/segments` — All 4,338 customers with RFM values and segment assignments
- `GET /api/elbow-method` — Inertia values for K=1 to K=10
- `GET /api/cluster-profiles` — Raw cluster profiles before naming

## Tech Stack
- Python 3.11
- FastAPI
- Pandas
- Scikit-learn
- Uvicorn

## Setup
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn main:app --reload`

## Deployment
Deployed on Render: `https://customer-segmentation-api-olf6.onrender.com`