import pandas as pd
from faker import Faker
import random
from datetime import datetime

fake = Faker()

# Load customer dimension data
customers_dimension_df = pd.read_csv('data/customers.csv')

# Ensure the customer_open_date is parsed as a datetime object with the correct format
customers_dimension_df['customer_open_date'] = pd.to_datetime(customers_dimension_df['customer_open_date'], format='%d/%m/%Y', dayfirst=True)

# Define the total number of records to generate
total_records = 100

def generate_internet_banking_activity(customers_df, total_records):
    data = []

    for _ in range(total_records):
        # Randomly select a customer
        customer = customers_df.sample(n=1).iloc[0]
        customer_id = customer['customer_id']
        open_date = customer['customer_open_date']

        # Generate a random event date after the customer's open date
        event_date = fake.date_between_dates(date_start=open_date, date_end=datetime.today())

        # Append the generated record to the data list
        data.append({
            'customer_id': customer_id,
            'event_date': event_date,
            'ibs_id': fake.uuid4(),
            'message': random.choice([
                'Logged in successfully',
                'Transfer funds',
                'Bill payment',
                'Password change',
                'Failed login attempt',
                'Account details updated'
            ]),
            'online_id': fake.random_number(digits=8),
            'source_ip_addr': fake.ipv4(),
            'session_key': fake.lexify(text='?' * 32),
            'service_type': random.choice(['web', 'mobile app'])
        })

    return data

# Generate internet banking activity data
activity_data = generate_internet_banking_activity(customers_dimension_df, total_records)

# Create a DataFrame from the generated data
df_internet_banking_activity = pd.DataFrame(activity_data)
print(df_internet_banking_activity.to_string())

# Save the generated data to a CSV file
internet_banking_csv_file = 'data/internet_banking_activity.csv'
df_internet_banking_activity.to_csv(internet_banking_csv_file, index=False)
