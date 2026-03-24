import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import json

def perform_analysis(features_file):
    df = pd.read_csv(features_file)
    user_ids = df['user_id']
    X = df.drop(['user_id', 'success_score'], axis=1)
    y = df['success_score']
    
    # 1. User Segmentation (Clustering)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Rename clusters creatively
    cluster_map = {0: 'Curious Explorers', 1: 'Power Builders', 2: 'Silent Drop-offs', 3: 'Collaborative Experts'}
    df['segment'] = df['cluster'].map(cluster_map)
    
    # 2. Predictive Modeling
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    # 3. Insights Generation
    insights = {
        "feature_importance": importances.to_dict(),
        "segment_stats": df.groupby('segment')['success_score'].mean().to_dict(),
        "aha_threshold": df[df['success_score'] > 80]['aha_latency_hrs'].median()
    }
    
    with open('insights.json', 'w') as f:
        json.dump(insights, f, indent=4)
        
    print("Analysis complete. Insights saved to insights.json")
    print("\nFeature Importance:")
    print(importances)
    
    return df, importances

if __name__ == "__main__":
    try:
        perform_analysis('behavioral_features.csv')
    except Exception as e:
        print(f"Error during analysis: {e}")
