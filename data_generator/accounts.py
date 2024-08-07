from faker import Faker
import random
import pandas as pd
import os

fake = Faker()

# Load customer dimension data
customers_dimension_df = pd.read_csv('data/customers.csv')


def generate_account_data(customers_df):
    accounts = []

    for _, customer in customers_df.iterrows():
        customer_id = customer['customer_id']
        account_usage = customer['customer_type']  # Use customer type to determine account usage
        num_accounts = random.randint(1, 3)  # Each customer can have 1-3 accounts

        for _ in range(num_accounts):
            account_type = random.choice([
                'Transaction', 'Savings', 'Home Loan', 'Credit Card',
                'Term Deposit', 'Personal Loan', 'Overdrafts',
                'Insurance', 'Investment', 'Superannuation'
            ])
            open_date = fake.date_this_century()

            accounts.append({
                'account_skey': fake.uuid4(),
                'customer_id': customer_id,
                'account_type': account_type,
                'product_code': account_type[:3].upper() + fake.bothify(text='##'),
                'account_number': fake.random_number(digits=10),
                'source_system': 'LMS' if account_type in ['Home Loan', 'Personal Loan', 'Overdraft'] else 'FIN' if account_type in ['Insurance','Investment', 'Superannuation'] else 'CC' if account_type == 'Credit Card' else 'CBS',
                'open_date': open_date.strftime('%d/%m/%Y'),
                'close_date': fake.date_between_dates(date_start=open_date).strftime('%d/%m/%Y') if random.choice([True, False]) else None,
                'last_card_activate_date': fake.date_between_dates(date_start=open_date).strftime('%d/%m/%Y')  if account_type in ['Transaction', 'Savings', 'Credit Card'] else '',
                'broker_introduced': random.choice(['Y', 'N']) if account_type in ['Home Loan', 'Personal Loan'] else '',
                'account_open_staff_id': fake.lexify(text='????'),
                'account_manager': fake.name() if account_usage == 'Business' else '',
                'risk_level': random.choice(['High', 'Low', 'Medium']),
                'account_usage': account_usage,
                'anzsic_code_desc': fake.lexify(text='????'),
                'interest_rate': round(random.uniform(2.0, 5.0), 2) if account_type in ['Home Loan', 'Personal Loan', 'Term Deposit', 'Savings'] else '',
                'account_limit': random.randint(1, 20) * 1000 if account_type in ['Transaction', 'Savings'] else '',
                'credit_limit': random.randint(1, 20) * 1000 if account_type in ['Credit Card', 'Overdrafts'] else '',
                'term_months': fake.random_int(min=1, max=60) if account_type in ['Home Loan', 'Personal Loan', 'Term Deposit'] else ''
            })

    return accounts

# Generate account dimension data
df_accounts = pd.DataFrame(generate_account_data(customers_dimension_df))
print(df_accounts.to_string())

data_directory = 'data'
csv_file = os.path.join(data_directory, 'accounts.csv')
os.makedirs(data_directory, exist_ok=True)
df_accounts.to_csv(csv_file, index=False)
