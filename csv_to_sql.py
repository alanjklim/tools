import pandas as pd

def csv_to_oracle_sql(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Extract column names
    columns = df.columns.tolist()
    
    # Prepare the base SQL template
    base_sql = "SELECT {} FROM DUAL"
    
    # Initialize a list to hold individual SELECT statements
    select_statements = []
    
    # Loop through each row in the DataFrame and create a SELECT statement
    for index, row in df.iterrows():
        values = ', '.join([f"'{str(value)}' AS {col}" for col, value in zip(columns, row)])
        select_statements.append(base_sql.format(values))
    
    # Combine all SELECT statements with UNION ALL
    union_all_sql = " UNION ALL ".join(select_statements)
    
    return union_all_sql

# Example usage
csv_file_path = 'data.csv'
sql_query = csv_to_oracle_sql(csv_file_path)
print(sql_query)
