from faker import Faker
import random
import pandas as pd

# Initialize Faker
fake = Faker('en_AU')

# Generate Customers Data
def generate_customers_data(num_records):
    customers = []
    for _ in range(num_records):
        customer_id = fake.unique.bothify(text='CU#####')
        first_name = fake.first_name()
        last_name = fake.last_name()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
        email = fake.email()
        phone_number = fake.phone_number()
        address = fake.address()
        customers.append({
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'email': email,
            'phone_number': phone_number,
            'address': address
        })
    return customers

# Generate Accounts Data
def generate_accounts_data(num_records, customer_ids):
    accounts = []
    account_types = ['Savings', 'Checking', 'Credit']
    for _ in range(num_records):
        account_id = fake.unique.bothify(text='AC#####')
        customer_id = random.choice(customer_ids)
        account_type = random.choice(account_types)
        balance = round(random.uniform(0, 100000), 2)
        date_opened = fake.date_this_decade()
        status = random.choice(['Active', 'Closed', 'Suspended'])
        accounts.append({
            'account_id': account_id,
            'customer_id': customer_id,
            'account_type': account_type,
            'balance': balance,
            'date_opened': date_opened,
            'status': status
        })
    return accounts

# Generate Products Data
def generate_products_data(num_records):
    products = []
    product_types = ['Loan', 'Deposit', 'Investment']
    for _ in range(num_records):
        product_id = fake.unique.bothify(text='PR#####')
        product_code = fake.bothify(text='PROD-##')
        product_name = fake.bs().title()
        product_type = random.choice(product_types)
        interest_rate = round(random.uniform(0, 10), 2)
        products.append({
            'product_id': product_id,
            'product_code': product_code,
            'product_name': product_name,
            'product_type': product_type,
            'interest_rate': interest_rate
        })
    return products

# Generate Transactions Data
def generate_transactions_data(num_records, account_ids, product_ids):
    transactions = []
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment']
    for _ in range(num_records):
        transaction_id = fake.unique.bothify(text='TR#####')
        account_id = random.choice(account_ids)
        product_id = random.choice(product_ids)
        transaction_date = fake.date_this_year()
        amount = round(random.uniform(1, 10000), 2)
        transaction_type = random.choice(transaction_types)
        transactions.append({
            'transaction_id': transaction_id,
            'account_id': account_id,
            'product_id': product_id,
            'transaction_date': transaction_date,
            'amount': amount,
            'transaction_type': transaction_type
        })
    return transactions

# Generate Internet Logs Data
def generate_internet_logs_data(num_records, customer_ids):
    internet_logs = []
    actions = ['LOGIN', 'LOGOUT', 'VIEW_ACCOUNT', 'TRANSFER', 'PAY_BILL']
    for _ in range(num_records):
        log_id = fake.unique.bothify(text='LG#####')
        customer_id = random.choice(customer_ids)
        ip_address = fake.ipv4()
        action = random.choice(actions)
        timestamp = fake.date_time_this_year()
        internet_logs.append({
            'log_id': log_id,
            'customer_id': customer_id,
            'ip_address': ip_address,
            'action': action,
            'timestamp': timestamp
        })
    return internet_logs

# Main function to generate all data
def generate_all_data(num_customers, num_accounts, num_products, num_transactions, num_internet_logs):
    customers = generate_customers_data(num_customers)
    customer_ids = [customer['customer_id'] for customer in customers]

    accounts = generate_accounts_data(num_accounts, customer_ids)
    account_ids = [account['account_id'] for account in accounts]

    products = generate_products_data(num_products)
    product_ids = [product['product_id'] for product in products]

    transactions = generate_transactions_data(num_transactions, account_ids, product_ids)
    internet_logs = generate_internet_logs_data(num_internet_logs, customer_ids)

    return {
        'customers': customers,
        'accounts': accounts,
        'products': products,
        'transactions': transactions,
        'internet_logs': internet_logs
    }

# Example usage
if __name__ == "__main__":
    data = generate_all_data(100, 200, 50, 500, 300)

    for table_name, records in data.items():
        df = pd.DataFrame(records)
        print(f"\n{table_name.upper()} TABLE")
        print(df.head())  # Print first 5 records for brevity

        # Optionally, save the data to CSV files
        df.to_csv(f"{table_name}.csv", index=False)
