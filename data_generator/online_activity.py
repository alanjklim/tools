import pandas as pd
from faker import Faker
import random

fake = Faker()

# Load customer dimension data
customers_dimension_df = pd.read_csv('/mnt/data/customers_dimension_table.csv')

def generate_internet_banking_activity(customers_df, num_records):
    data = []
    
    for _ in range(num_records):
        customer_id = random.choice(customers_df['customer_id'].tolist())
        event_date = fake.date_this_century().strftime('%d/%m/%Y')
        ibs_id = fake.unique.random_int(min=1000, max=9999)
        message = random.choice([
            'Logged in successfully',
            'Transfer funds',
            'Bill payment',
            'Password change',
            'Failed login attempt',
            'Account details updated'
        ])
        online_id = fake.random_number(digits=8)
        customer_name = random.choice(customers_df['full_name'].tolist())
        source_ip_addr = fake.ipv4()
        session_key = fake.uuid4()
        service_type = random.choice(['web', 'mobile app'])
        effective_date = fake.date_this_century().strftime('%d/%m/%Y')
        
        data.append([
            customer_id,
            event_date,
            ibs_id,
            message,
            online_id,
            customer_name,
            source_ip_addr,
            session_key,
            service_type,
            effective_date
        ])
    
    columns = [
        'customer_id',
        'event_date',
        'ibs_id',
        'message',
        'online_id',
        'customer_name',
        'source_ip_addr',
        'session_key',
        'service_type',
        'effective_date'
    ]
    
    return pd.DataFrame(data, columns=columns)

# Generate internet banking activity data
df_internet_banking_activity = generate_internet_banking_activity(customers_dimension_df, 100)

# Save the DataFrame to a CSV file
csv_file_path = '/mnt/data/internet_banking_activity.csv'
df_internet_banking_activity.to_csv(csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Internet Banking Activity Data", dataframe=df_internet_banking_activity)

csv_file_path
