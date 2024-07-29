import pandas as pd
from faker import Faker
import random

fake = Faker()

# Load customer and account dimension data
customers_dimension_df = pd.read_csv('/mnt/data/customers_dimension_table.csv')
accounts_dimension_df = pd.read_csv('/mnt/data/accounts_dimension_table.csv')

def generate_fact_transactions(customers_df, accounts_df, num_records):
    data = []
    
    for _ in range(num_records):
        effective_date = fake.date_this_century().strftime('%d/%m/%Y')
        transaction_date = fake.date_this_century().strftime('%d/%m/%Y')
        account = accounts_df.sample(1).iloc[0]
        account_number = account['account_number']
        source_system = account['source_system']
        transaction_amount = round(random.uniform(10.0, 1000.0), 2)
        trans_narration_code = fake.random_number(digits=4)
        trans_source_code = fake.lexify(text='??')
        trans_type_code = random.choice(['deposit', 'withdraw', 'narration', 'interest', 'transfer'])
        product_code = fake.lexify(text='????')
        card_number = fake.random_number(digits=16)
        transfer_bsb_number = fake.bban()
        transfer_account_num = fake.random_number(digits=10)
        transaction_narration = fake.sentence(nb_words=6)
        credit_debit_flag = random.choice(['credit', 'debit'])
        customer_id = account['customer_id']
        
        data.append([
            effective_date,
            transaction_date,
            account_number,
            source_system,
            transaction_amount,
            trans_narration_code,
            trans_source_code,
            trans_type_code,
            product_code,
            card_number,
            transfer_bsb_number,
            transfer_account_num,
            transaction_narration,
            credit_debit_flag,
            customer_id
        ])
    
    columns = [
        'effective_date',
        'transaction_date',
        'account_number',
        'source_system',
        'transaction_amount',
        'trans_narration_code',
        'trans_source_code',
        'trans_type_code',
        'product_code',
        'card_number',
        'transfer_bsb_number',
        'transfer_account_num',
        'transaction_narration',
        'credit_debit_flag',
        'customer_id'
    ]
    
    return pd.DataFrame(data, columns=columns)

# Generate fact transactions data
df_fact_transactions = generate_fact_transactions(customers_dimension_df, accounts_dimension_df, 100)

# Save the DataFrame to a CSV file
csv_file_path = '/mnt/data/fact_transactions.csv'
df_fact_transactions.to_csv(csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Fact Transactions Data", dataframe=df_fact_transactions)

csv_file_path
