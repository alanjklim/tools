import pandas as pd
from faker import Faker
import random

fake = Faker()

# Load customer and account dimension data
customers_dimension_df = pd.read_csv('data/customers.csv')
accounts_dimension_df = pd.read_csv('data/accounts.csv')

def generate_fact_transactions(customers_df, accounts_df, num_records):
    data = []

    for _ in range(num_records):
        # Sample a single account from the accounts_df
        account = accounts_df.sample(1).iloc[0]

        # Append the transaction data using the sampled account details
        data.append({
            'effective_date': fake.date_this_century().strftime('%d/%m/%Y'),
            'transaction_date': fake.date_this_century().strftime('%d/%m/%Y'),
            'account_number': account['account_number'],
            'source_system': account['source_system'],  # Get source system from the sampled account
            'transaction_amount': round(random.uniform(10.0, 1000.0), 2),
            'trans_narration_code': fake.random_number(digits=4),
            'trans_source_code': fake.lexify(text='??'),
            'trans_type_code': random.choice(['deposit', 'withdraw', 'narration', 'interest', 'transfer']),
            'product_code': account['product_code'],  # Get product code from the sampled account
            'card_number': fake.random_number(digits=16),
            'transfer_bsb_number': fake.bban(),
            'transfer_account_num': fake.random_number(digits=10),
            'transaction_narration': fake.sentence(nb_words=6),
            'credit_debit_flag': random.choice(['credit', 'debit']),
            'customer_id': account['customer_id']  # Get customer ID from the sampled account
        })

    return pd.DataFrame(data)

# Generate fact transactions data
df_fact_transactions = generate_fact_transactions(customers_dimension_df, accounts_dimension_df, 100)
print(df_fact_transactions.to_string())

# Save the generated data to a CSV file
df_fact_transactions.to_csv('data/fact_transactions.csv', index=False)
