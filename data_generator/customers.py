from faker import Faker
from datetime import date, timedelta
import pandas as pd
import random
import os

# Initialize Faker
fake = Faker('en_AU')
num_customers = 10

# Mapping of postcode first digit to state and area code
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

def get_postcode_state():
    valid_first_digits = list(postcode_to_state.keys())
    first_digit = random.choice(valid_first_digits)
    postcode = fake.numerify(text=f"{first_digit}###")
    state_area_info = postcode_to_state.get(first_digit, {'state': 'Unknown', 'area_code': ''})
    return postcode, state_area_info['state'], state_area_info['area_code']

def generate_customers(num_records):
    customers = []
    for _ in range(num_records):
        dob = fake.date_of_birth(minimum_age=1, maximum_age=100)  # dob is a date object
        age = (date.today() - dob).days // 365  # Calculate age by subtracting dob from today
        open_date = fake.date_between_dates(date_start=dob, date_end=date.today())  # Open date between dob and today
        deceased = random.choice(['N', 'Y'])
        postcode, state, area_code = get_postcode_state()
        gender = random.choice(['M', 'F', 'Other'])

        # Determine customer type, enforce "Personal" if age < 18
        customer_type = 'Personal' if age < 18 else random.choice(['Business', 'Personal'])

        customer = {
            'customer_id': 'CUST-' + fake.uuid4(),
            'customer_type': customer_type,
            'first_name': fake.first_name_male() if gender == 'M' else fake.first_name_female() if gender == 'F' else fake.first_name(),
            'surname': fake.last_name(),
            'dob': dob.strftime('%d/%m/%Y'),
            'customer_age': age,
            'deceased_indicator': deceased,
            'gender': gender,
            'res_phone': f"{area_code} {fake.numerify(text='#### ####')}",
            'bus_phone': f"{area_code} {fake.numerify(text='#### ####')}" if customer_type == 'Business' else '',
            'customer_open_date': open_date.strftime('%d/%m/%Y'),
            'customer_close_date': customer_close_date,
            'residential_address': fake.street_address(),
            'residential_suburb': fake.city(),
            'residential_state': state,
            'residential_postcode': postcode,
        }
        customers.append(customer)
    return customers

# Generate the customers list
customers_df = pd.DataFrame(generate_customers(num_customers))

# Print the DataFrame to the terminal
print(customers_df.to_string())

# Save the DataFrame to a CSV file
data_directory = 'data'
csv_file = os.path.join(data_directory, 'customers.csv')
os.makedirs(data_directory, exist_ok=True)
customers_df.to_csv(csv_file, index=False)
