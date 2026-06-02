from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-computed data files
df_country = pd.read_csv("country_distribution.csv")
df_monthly = pd.read_csv("monthly_revenue.csv")
df_cumulative = pd.read_csv("cumulative_revenue.csv")
rfm = pd.read_csv("rfm_segments.csv", dtype={'CustomerID': str})
segment_summary = pd.read_csv("segment_summary.csv")

@app.get("/")
def root():
    return {"message": "Customer Segmentation API is running!"}

@app.get("/api/segment-summary")
def get_segment_summary():
    return segment_summary.to_dict(orient="records")

@app.get("/api/segments")
def get_segments():
    return rfm.to_dict(orient="records")

@app.get("/api/country-distribution")
def get_country_distribution():
    return df_country.to_dict(orient="records")

@app.get("/api/monthly-revenue")
def get_monthly_revenue():
    return df_monthly.to_dict(orient="records")

@app.get("/api/cumulative-revenue")
def get_cumulative_revenue():
    return df_cumulative.to_dict(orient="records")
@app.get("/api/cleaning-summary")
def get_cleaning_summary():
    return [
        {"step": "Raw dataset", "rows": 541909, "removed": 0, "reason": ""},
        {"step": "Remove missing CustomerID", "rows": 406829, "removed": 135080, "reason": "Guest checkouts — cannot identify customer"},
        {"step": "Remove returns", "rows": 397924, "removed": 8905, "reason": "Negative quantities indicate returned orders"},
        {"step": "Remove bad prices", "rows": 397884, "removed": 40, "reason": "Zero or negative unit prices — data errors"},
    ]

@app.get("/api/elbow-method")
def get_elbow_method():
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    import numpy as np

    # Recreate RFM scaled
    rfm_data = rfm[['Recency', 'Frequency', 'Monetary']].copy()
    rfm_data['Recency_log'] = np.log1p(rfm_data['Recency'])
    rfm_data['Frequency_log'] = np.log1p(rfm_data['Frequency'])
    rfm_data['Monetary_log'] = np.log1p(rfm_data['Monetary'])

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_data[['Recency_log', 'Frequency_log', 'Monetary_log']])

    inertias = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(rfm_scaled)
        inertias.append({"k": k, "inertia": round(kmeans.inertia_, 1)})

    return inertias

@app.get("/api/cluster-profiles")
def get_cluster_profiles():
    cluster_profiles = rfm.groupby('Cluster').agg(
        Avg_Recency=('Recency', 'mean'),
        Avg_Frequency=('Frequency', 'mean'),
        Avg_Monetary=('Monetary', 'mean'),
        Customers=('CustomerID', 'count')
    ).round(1).reset_index()
    return cluster_profiles.to_dict(orient="records")