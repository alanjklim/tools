import pandas as pd
from faker import Faker
import random

fake = Faker()

# Load customer and account dimension data
customers_dimension_df = pd.read_csv('/mnt/data/customers_dimension_table.csv')
accounts_dimension_df = pd.read_csv('/mnt/data/accounts_dimension_table.csv')

def generate_customer_account_map(customers_df, accounts_df, num_records):
    data = []
    
    for _ in range(num_records):
        cust_acct_skey = fake.unique.random_int(min=1, max=100000)
        customer_id = random.choice(customers_df['customer_id'].tolist())
        account = accounts_df.sample(1).iloc[0]
        source_system = account['source_system']
        account_number = account['account_number']
        cust_acct_rel_type = random.choice(['own', 'joint', 'guarantor', 'signatory'])
        primary_cust_flag = random.choice(['y', 'n'])
        valid_from_date = fake.date_this_century().strftime('%d/%m/%Y')
        valid_to_date = fake.date_this_century().strftime('%d/%m/%Y')
        effective_status = random.choice(['open', 'close', 'delete'])
        
        data.append([
            cust_acct_skey,
            customer_id,
            source_system,
            account_number,
            cust_acct_rel_type,
            primary_cust_flag,
            valid_from_date,
            valid_to_date,
            effective_status
        ])
    
    columns = [
        'cust_acct_skey',
        'customer_id',
        'source_system',
        'account_number',
        'cust_acct_rel_type',
        'primary_cust_flag',
        'valid_from_date',
        'valid_to_date',
        'effective_status'
    ]
    
    return pd.DataFrame(data, columns=columns)

# Generate customer account map data
df_customer_account_map = generate_customer_account_map(customers_dimension_df, accounts_dimension_df, 100)

# Save the DataFrame to a CSV file
csv_file_path = '/mnt/data/customer_account_map.csv'
df_customer_account_map.to_csv(csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Customer Account Map Data", dataframe=df_customer_account_map)

csv_file_path
