import csv
from datetime import datetime, timedelta
import uuid
import random

def generate_zerve_data(num_users=500, days=90):
    random.seed(42)
    
    event_types = [
        'login', 'create_notebook', 'execute_cell', 'import_library',
        'install_package', 'share_project', 'add_collaborator',
        'export_data', 'deploy_api', 'create_canvas', 'connect_nodes',
        'comment_on_cell', 'version_commit'
    ]
    
    # User archetypes
    archetypes = ['Power Builder', 'Curious Explorer', 'Silent Drop-off', 'Collaborative Expert']
    user_pool = []
    
    for _ in range(num_users):
        u_id = str(uuid.uuid4())[:8]
        arch = random.choice(archetypes)
        signup_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 30))
        user_pool.append({'user_id': u_id, 'archetype': arch, 'signup_date': signup_date})
    
    events = []
    for user in user_pool:
        u_id = user['user_id']
        arch = user['archetype']
        curr_date = user['signup_date']
        
        # Determine activity span based on archetype
        if arch == 'Power Builder':
            activity_days = days
            freq_range = (5, 15)
        elif arch == 'Curious Explorer':
            activity_days = random.randint(10, 40)
            freq_range = (3, 8)
        elif arch == 'Collaborative Expert':
            activity_days = days
            freq_range = (8, 20)
        else: # Silent Drop-off
            activity_days = random.randint(1, 5)
            freq_range = (1, 4)
            
        for d in range(activity_days):
            date = curr_date + timedelta(days=d)
            if date > datetime(2025, 4, 1): break
            
            # Daily events
            daily_count = random.randint(*freq_range) if random.random() > 0.3 else 0
            for _ in range(daily_count):
                # Simple weight-based selection without numpy
                if arch == 'Power Builder':
                    choices = event_types + ['execute_cell'] * 10 + ['deploy_api'] * 2
                elif arch == 'Collaborative Expert':
                    choices = event_types + ['add_collaborator'] * 5 + ['share_project'] * 5
                else:
                    choices = event_types
                
                event = random.choice(choices)
                events.append({
                    'timestamp': (date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))).isoformat(),
                    'user_id': u_id,
                    'event_type': event,
                    'session_id': str(uuid.uuid4())[:12]
                })

    # Write to CSV using standard module
    with open('user_events.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'user_id', 'event_type', 'session_id'])
        writer.writeheader()
        writer.writerows(events)
        
    print(f"Generated {len(events)} events for {num_users} users.")

if __name__ == "__main__":
    generate_zerve_data()
