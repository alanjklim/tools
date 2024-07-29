from faker import Faker
import random
import pandas as pd

fake = Faker()

def generate_customer_data(num_records):
    data = []
    
    for _ in range(num_records):
        customer_id = fake.bothify(text='??#####')
        customer_type = random.choice(['Business', 'Personal'])
        surname = fake.last_name()
        first_name = fake.first_name()
        full_name = f"{first_name} {surname}"
        country_of_residence = 'Australia'
        customer_age = random.randint(18, 90)
        deceased_indicator = random.choice(['Y', 'N'])
        gender = random.choice(['M', 'F', 'Other'])
        address = fake.street_address()
        suburb = fake.city()
        state = fake.state_abbr()
        postcode = fake.postcode()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d/%m/%Y')
        phone = fake.phone_number()
        customer_open_date = fake.date_this_century().strftime('%d/%m/%Y')
        
        data.append([
            customer_id,
            customer_type,
            surname,
            first_name,
            full_name,
            country_of_residence,
            customer_age,
            deceased_indicator,
            gender,
            address,
            suburb,
            state,
            postcode,
            dob,
            phone,
            customer_open_date
        ])
    
    columns = [
        'customer_id',
        'customer_type',
        'surname',
        'first_name',
        'full_name',
        'country_of_residence',
        'customer_age',
        'deceased_indicator',
        'gender',
        'address',
        'suburb',
        'state',
        'postcode',
        'dob',
        'phone',
        'customer_open_date'
    ]
    
    return pd.DataFrame(data, columns=columns)

# Generate 10 records of customer data
df_customers = generate_customer_data(10)

# Save the DataFrame to a CSV file
csv_file_path = '/mnt/data/customers_data.csv'
df_customers.to_csv(csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Customer Data", dataframe=df_customers)

print(f"Customer data saved to {csv_file_path}")
