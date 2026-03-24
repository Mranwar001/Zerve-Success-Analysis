import csv
from datetime import datetime, timedelta
from collections import defaultdict

def engineer_features(events_file, metrics_file):
    # Load events
    user_events = defaultdict(list)
    with open(events_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_events[row['user_id']].append({
                'timestamp': datetime.fromisoformat(row['timestamp']),
                'event_type': row['event_type'],
                'session_id': row['session_id']
            })
            
    # Load success metrics (for labels)
    success_map = {}
    with open(metrics_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            success_map[row['user_id']] = float(row['success_score'])
            
    features = []
    advanced_events = {'deploy_api', 'share_project', 'add_collaborator', 'export_data', 'version_commit', 'create_canvas'}
    
    for u_id, events in user_events.items():
        events.sort(key=lambda x: x['timestamp'])
        first_ts = events[0]['timestamp']
        
        # F1: Time to first advanced action (Aha Moment)
        aha_ts = next((e['timestamp'] for e in events if e['event_type'] in advanced_events), None)
        aha_latency_hours = (aha_ts - first_ts).total_seconds() / 3600 if aha_ts else 2160 # Penalty for no aha
        
        # F2: Workflow Diversity
        unique_events = len(set(e['event_type'] for e in events))
        
        # F3: Session Intensity (events per session)
        sessions = defaultdict(int)
        for e in events:
            sessions[e['session_id']] += 1
        avg_session_intensity = sum(sessions.values()) / len(sessions)
        
        # F4: Quick-Start Ratio (events in first 24h / total)
        day1_count = sum(1 for e in events if e['timestamp'] < first_ts + timedelta(days=1))
        quick_start_ratio = day1_count / len(events)
        
        # F5: Collaboration Focus
        collab_events = {'share_project', 'add_collaborator', 'comment_on_cell'}
        collab_count = sum(1 for e in events if e['event_type'] in collab_events)
        collab_ratio = collab_count / len(events)
        
        features.append({
            'user_id': u_id,
            'aha_latency_hrs': round(aha_latency_hours, 2),
            'unique_event_types': unique_events,
            'avg_session_intensity': round(avg_session_intensity, 2),
            'quick_start_ratio': round(quick_start_ratio, 4),
            'collab_ratio': round(collab_ratio, 4),
            'total_sessions': len(sessions),
            'success_score': success_map.get(u_id, 0)
        })
        
    with open('behavioral_features.csv', 'w', newline='') as f:
        fields = ['user_id', 'aha_latency_hrs', 'unique_event_types', 'avg_session_intensity', 'quick_start_ratio', 'collab_ratio', 'total_sessions', 'success_score']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(features)
        
    print(f"Engineered features for {len(features)} users.")

if __name__ == "__main__":
    engineer_features('user_events.csv', 'user_success_metrics.csv')
