from faker import Faker
import pandas as pd
import random
import os

fake = Faker('en_AU')

# Read the customer data from customers_with_addresses.csv
customers_df = pd.read_csv('data/customers_with_addresses.csv')


def create_address_row(customer_id, address_type, address, suburb, state, postcode):
    return {
        'customer_id': customer_id,
        'address_type': address_type,
        'full_address': f"{address}, {suburb}, {state} {postcode}",
        'address': address,
        'suburb': suburb,
        'state': state,
        'postcode': postcode,
        'country_of_residence': 'Australia',
        'res_addr_indicator': 'Y' if address_type == 'Residential' else 'N',
        'valid_from_date': fake.date_this_century().strftime('%d/%m/%Y'),
        'valid_to_date': fake.date_this_century().strftime('%d/%m/%Y'),
        'effective_status': random.choice(['Active', 'Inactive', 'Deleted']),
        'mosaic_code': fake.lexify(text='????'),
        'geolocation_lat': fake.latitude(),
        'geolocation_long': fake.longitude()
    }


def generate_address_rows(customers_df):
    addresses = []

    for _, customer in customers_df.iterrows():
        customer_id = customer['customer_id']

        # Add Residential address row if available
        if pd.notna(customer['residential_address']):
            addresses.append(create_address_row(
                customer_id,
                'Residential',
                customer['residential_address'],
                customer['residential_suburb'],
                customer['residential_state'],
                customer['residential_postcode']
            ))

        # Add Business address row if available
        if pd.notna(customer['business_address']):
            addresses.append(create_address_row(
                customer_id,
                'Business',
                customer['business_address'],
                customer['business_suburb'],
                customer['business_state'],
                customer['business_postcode']
            ))

        # Add PO Box address row if available
        if pd.notna(customer['po_address']):
            addresses.append(create_address_row(
                customer_id,
                'PO Box',
                customer['po_address'],
                customer['po_suburb'],
                customer['po_state'],
                customer['po_postcode']
            ))

    return addresses


# Generate the addresses as rows
address_rows = generate_address_rows(customers_df)

# Create a DataFrame for the addresses
address_df = pd.DataFrame(address_rows).sort_values(by='customer_id')

# Print the DataFrame to the console
print(address_df.to_string())

# Save the DataFrame to a CSV file
# data_directory = 'data'
# csv_file = os.path.join(data_directory, 'addresses.csv')
# os.makedirs(data_directory, exist_ok=True)
# address_df.to_csv(csv_file, index=False)
