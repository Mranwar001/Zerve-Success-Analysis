import csv
from datetime import datetime, timedelta
from collections import defaultdict

def calculate_success_score(events_file):
    user_events = defaultdict(list)
    with open(events_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_events[row['user_id']].append({
                'timestamp': datetime.fromisoformat(row['timestamp']),
                'event_type': row['event_type'],
                'session_id': row['session_id']
            })
            
    success_data = []
    advanced_events = {'deploy_api', 'share_project', 'add_collaborator', 'export_data', 'version_commit'}
    
    for u_id, events in user_events.items():
        events.sort(key=lambda x: x['timestamp'])
        first_event = events[0]['timestamp']
        last_event = events[-1]['timestamp']
        
        # 1. Retention Score (0-30) - Active weeks
        active_weeks = len(set(e['timestamp'].isocalendar()[1] for e in events))
        retention_score = min(30, (active_weeks / 12) * 30)
        
        # 2. Depth Score (0-30) - Advanced feature usage
        adv_count = sum(1 for e in events if e['event_type'] in advanced_events)
        total_count = len(events)
        depth_score = min(30, (adv_count / (total_count * 0.1 + 1)) * 30) # Baseline 10% advanced
        
        # 3. Complexity Score (0-20) - Distinct session activity
        unique_sessions = len(set(e['session_id'] for e in events))
        complexity_score = min(20, (unique_sessions / 50) * 20)
        
        # 4. Velocity Score (0-20) - Event growth in first 30 days vs next
        first_month = [e for e in events if e['timestamp'] < first_event + timedelta(days=30)]
        second_month = [e for e in events if first_event + timedelta(days=30) <= e['timestamp'] < first_event + timedelta(days=60)]
        
        v1 = len(first_month)
        v2 = len(second_month)
        velocity_ratio = (v2 / (v1 + 1))
        velocity_score = min(20, velocity_ratio * 10) # 1.0 ratio = 10 pts, 2.0 = 20 pts
        
        total_score = retention_score + depth_score + complexity_score + velocity_score
        
        success_data.append({
            'user_id': u_id,
            'retention_score': round(retention_score, 2),
            'depth_score': round(depth_score, 2),
            'complexity_score': round(complexity_score, 2),
            'velocity_score': round(velocity_score, 2),
            'success_score': round(total_score, 2),
            'total_events': total_count,
            'days_active': (last_event - first_event).days + 1
        })
        
    # Write success scores
    with open('user_success_metrics.csv', 'w', newline='') as f:
        fields = ['user_id', 'retention_score', 'depth_score', 'complexity_score', 'velocity_score', 'success_score', 'total_events', 'days_active']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(success_data)
        
    print(f"Calculated success scores for {len(success_data)} users.")

if __name__ == "__main__":
    calculate_success_score('user_events.csv')
