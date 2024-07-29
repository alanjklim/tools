import pandas as pd
from faker import Faker
import random

fake = Faker()

# Load customer dimension data
customers_dimension_df = pd.read_csv('/mnt/data/customers_dimension_table.csv')

def generate_address_data(customers_df, num_records):
    data = []
    
    for _ in range(num_records):
        cust_addr_skey = fake.unique.random_int(min=1, max=100000)
        customer_id = random.choice(customers_df['customer_id'].tolist())
        address_type = random.choice(['residential', 'po box', 'personal', 'business'])
        address_effective_date = fake.date_this_century().strftime('%d/%m/%Y')
        full_address = fake.address().replace("\n", ", ")
        address = fake.street_address()
        suburb = fake.city()
        state = fake.state_abbr()
        postcode = fake.postcode()
        res_addr_indicator = random.choice(['y', 'n'])
        country_of_residence = 'Australia'
        valid_from_date = fake.date_this_century().strftime('%d/%m/%Y')
        valid_to_date = fake.date_this_century().strftime('%d/%m/%Y')
        effective_status = random.choice(['active', 'inactive', 'deleted'])
        mosaic_code = fake.lexify(text='????')
        geolocation_id = fake.uuid4()
        geolocation_lat = fake.latitude()
        geolocation_long = fake.longitude()
        
        data.append([
            cust_addr_skey,
            customer_id,
            address_type,
            address_effective_date,
            full_address,
            address,
            suburb,
            state,
            postcode,
            res_addr_indicator,
            country_of_residence,
            valid_from_date,
            valid_to_date,
            effective_status,
            mosaic_code,
            geolocation_id,
            geolocation_lat,
            geolocation_long
        ])
    
    columns = [
        'cust_addr_skey',
        'customer_id',
        'address_type',
        'address_effective_date',
        'full_address',
        'address',
        'suburb',
        'state',
        'postcode',
        'res_addr_indicator',
        'country_of_residence',
        'valid_from_date',
        'valid_to_date',
        'effective_status',
        'mosaic_code',
        'geolocation_id',
        'geolocation_lat',
        'geolocation_long'
    ]
    
    return pd.DataFrame(data, columns=columns)

# Generate address dimension data
df_addresses = generate_address_data(customers_dimension_df, 100)

# Save the DataFrame to a CSV file
csv_file_path = '/mnt/data/address_dimension_table.csv'
df_addresses.to_csv(csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Address Dimension Data", dataframe=df_addresses)

csv_file_path
