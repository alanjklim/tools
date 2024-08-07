from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import random
import os

fake = Faker('en_AU')
num_customers = 10

postcode_to_state = {
    '2': {'state': 'NSW', 'area_code': '02'},
    '3': {'state': 'VIC', 'area_code': '03'},
    '4': {'state': 'QLD', 'area_code': '07'},
    '5': {'state': 'SA', 'area_code': '08'},
    '6': {'state': 'WA', 'area_code': '08'},
    '7': {'state': 'TAS', 'area_code': '03'},
    '8': {'state': 'NT', 'area_code': '08'},
    '0': {'state': 'ACT', 'area_code': '02'}
}

def calculate_age(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, '%d/%m/%Y')
    return relativedelta(today, dob).years

def get_postcode_state():
    valid_first_digits = list(postcode_to_state.keys())
    first_digit = random.choice(valid_first_digits)
    postcode = fake.numerify(text=f"{first_digit}###")
    state_area_info = postcode_to_state.get(first_digit, {'state': 'Unknown', 'area_code': ''})
    return postcode, state_area_info['state'], state_area_info['area_code']

def customer_open_date(dob):
    dob_date = datetime.strptime(dob, '%d/%m/%Y')
    min_open_date = dob_date + relativedelta(years=1)
    return fake.date_between_dates(date_start=min_open_date, date_end=datetime.today()).strftime('%d/%m/%Y')

def generate_customers_with_addresses(num_records):
    customers = []
    for _ in range(num_records):
        dob = fake.date_of_birth(minimum_age=1, maximum_age=100).strftime('%d/%m/%Y')
        age = calculate_age(dob)
        gender = random.choice(['M', 'F', 'Other'])
        postcode, state, area_code = get_postcode_state()

        # Determine customer type, enforce "Personal" if age < 18
        customer_type = 'Personal' if age < 18 else random.choice(['Business', 'Personal'])

        # Generate residential address
        residential_address = fake.street_address()
        residential_suburb = fake.city()
        residential_postcode = postcode
        residential_state = state

        # Generate business address if customer is Business
        business_address = ''
        business_suburb = ''
        business_state = ''
        business_postcode = ''
        if customer_type == 'Business':
            business_address = fake.street_address()
            business_suburb = fake.city()
            business_state = state
            business_postcode = f"{postcode[0]}{fake.numerify(text='###')}"

        # Generate PO Box address
        po_address = ''
        po_suburb = ''
        po_state = ''
        po_postcode = ''
        if random.choice([True, False]):  # Randomly decide if there's a PO Box
            po_address = f"PO Box {fake.building_number()}"
            po_suburb = fake.city()
            po_state = state
            po_postcode = f"{postcode[0]}{fake.numerify(text='###')}"

        customer = {
            'customer_id': 'CUST-' + fake.uuid4(),
            'customer_type': customer_type,
            'first_name': fake.first_name_male() if gender == 'M' else fake.first_name_female() if gender == 'F' else fake.first_name(),
            'surname': fake.last_name(),
            'dob': dob,
            'customer_age': age,
            'deceased_indicator': random.choice(['Y', 'N']),
            'gender': gender,
            'res_phone': f"{area_code} {fake.numerify(text='#### ####')}",
            'bus_phone': f"{area_code} {fake.numerify(text='#### ####')}" if customer_type == 'Business' else '',
            'customer_open_date': customer_open_date(dob),
            'residential_address': residential_address,
            'residential_suburb': residential_suburb,
            'residential_state': residential_state,
            'residential_postcode': residential_postcode,
            'business_address': business_address,
            'business_suburb': business_suburb,
            'business_state': business_state,
            'business_postcode': business_postcode,
            'po_address': po_address,
            'po_suburb': po_suburb,
            'po_state': po_state,
            'po_postcode': po_postcode
        }
        customers.append(customer)
    return customers

customers_df = pd.DataFrame(generate_customers_with_addresses(num_customers))
print(customers_df.to_string())

# data_directory = 'data'
# csv_file = os.path.join(data_directory, 'customers_with_addresses.csv')
# os.makedirs(data_directory, exist_ok=True)
# customers_df.to_csv(csv_file, index=False)
