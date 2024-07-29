from faker import Faker
import random
import pandas as pd

fake = Faker()

# Load customer dimension data
customers_dimension_df = pd.read_csv('/mnt/data/customers_dimension_table.csv')

def generate_account_data(customers_df, num_records):
    data = []
    
    for _ in range(num_records):
        account_skey = fake.unique.random_int(min=1, max=100000)
        customer_id = random.choice(customers_df['customer_id'].tolist())
        source_system = random.choice(['everyday', 'home loan', 'credit cards', 'term deposit'])
        account_number = fake.random_number(digits=10)
        open_date = fake.date_this_century().strftime('%d/%m/%Y')
        valid_from_date = fake.date_this_century().strftime('%d/%m/%Y')
        valid_to_date = fake.date_this_century().strftime('%d/%m/%Y')
        effective_status = random.choice(['open', 'close', 'delete'])
        card_last_activate_date = None
        broker_introduced = random.choice(['y', 'n'])
        currency = fake.currency_code()
        account_open_staff_id = fake.lexify(text='????')
        close_date = None
        account_usage_code = random.choice(['Business', 'Personal'])
        anzsic_code_desc = fake.lexify(text='????')
        
        term_months = term_days = remaining_term = interest_payment_freq = None
        
        if source_system == 'credit cards':
            card_last_activate_date = fake.date_this_century().strftime('%d/%m/%Y')
        elif source_system in ['home loan', 'term deposit']:
            term_months = fake.random_int(min=1, max=60)
            term_days = term_months * 30
            remaining_term = fake.random_int(min=0, max=term_days)
            interest_payment_freq = random.choice(['Monthly', 'Quarterly', 'Yearly'])
        
        data.append([
            account_skey,
            customer_id,
            source_system,
            account_number,
            open_date,
            valid_from_date,
            valid_to_date,
            effective_status,
            card_last_activate_date,
            broker_introduced,
            currency,
            account_open_staff_id,
            close_date,
            account_usage_code,
            anzsic_code_desc,
            term_months,
            term_days,
            remaining_term,
            interest_payment_freq,
            effective_status
        ])
    
    columns = [
        'account_skey',
        'customer_id',
        'source_system',
        'account_number',
        'open_date',
        'valid_from_date',
        'valid_to_date',
        'effective_status',
        'card_last_activate_date',
        'broker_introduced',
        'currency',
        'account_open_staff_id',
        'close_date',
        'account_usage_code',
        'anzsic_code_desc',
        'term_months',
        'term_days',
        'remaining_term',
        'interest_payment_freq',
        'effective_status'
    ]
    
    return pd.DataFrame(data, columns=columns)

# Generate account dimension data
df_accounts = generate_account_data(customers_dimension_df, 100)

# Save the DataFrame to a CSV file
csv_file_path = '/mnt/data/accounts_dimension_table.csv'
df_accounts.to_csv(csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Accounts Dimension Data", dataframe=df_accounts)

csv_file_path
