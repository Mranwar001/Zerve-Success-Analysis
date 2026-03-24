import json
import sys

def predict_success(aha_latency, quick_start_ratio, total_sessions, unique_events):
    # Simplified model based on Random Forest feature importance
    # 92% Weight on sessions, 4% Aha Latency, 2% Quick Start, 2% Diversity
    
    # Normalize inputs (based on 500-user distribution)
    s_score = min(100, (total_sessions / 500) * 100) * 0.92
    a_score = max(0, (1 - (aha_latency / 2160))) * 100 * 0.04
    q_score = (quick_start_ratio) * 100 * 0.02
    d_score = (unique_events / 13) * 100 * 0.02
    
    total = s_score + a_score + q_score + d_score
    return round(total, 2)

if __name__ == "__main__":
    print("--- Zerve Success Prediction Tool ---")
    print("This tool predicts the probability of long-term success based on early behavioral signals.")
    
    try:
        aha = float(input("Time to reach 'Aha Moment' (Hours until first advanced action): "))
        qsr = float(input("Quick Start Ratio (Activity in first 24h / total activity): "))
        sessions = int(input("Total sessions in the first 30 days: "))
        div = int(input("Number of unique features explore (1-13): "))
        
        prob = predict_success(aha, qsr, sessions, div)
        
        print(f"\nPredicted Success Score: {prob}/100")
        if prob > 80:
            print("Status: HIGH POTENTIAL POWER USER")
        elif prob > 50:
            print("Status: STEADY GROWER")
        else:
            print("Status: HIGH CHURN RISK - ACTION REQUIRED")
            
    except ValueError:
        print("Invalid input. Please enter numeric values.")
