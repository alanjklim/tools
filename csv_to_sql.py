import pandas as pd

def detect_data_type(value):
    """Detects the SQL-friendly data type of a value."""
    if pd.isna(value):
        return "NULL"
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        return str(value)
    elif isinstance(value, pd.Timestamp):
        return f"TO_DATE('{value}', 'YYYY-MM-DD HH24:MI:SS')"
    else:
        return f"'{str(value).replace('\'', '\'\'')}'"

def csv_to_cte_sql(csv_file_path, cte_name='data_cte', chunk_size=1000):
    """Converts a CSV file into an Oracle SQL CTE with dynamic data type handling and chunk processing."""
    cte_sql = f"WITH {cte_name} AS ("
    
    # Read the CSV file in chunks
    chunks = pd.read_csv(csv_file_path, chunksize=chunk_size)
    
    select_statements = []
    for chunk in chunks:
        columns = chunk.columns.tolist()
        for index, row in chunk.iterrows():
            values = ', '.join([f"{detect_data_type(value)} AS {col}" for col, value in zip(columns, row)])
            select_statements.append(f"SELECT {values} FROM DUAL")
    
    # Combine all SELECT statements with UNION ALL
    union_all_sql = " UNION ALL ".join(select_statements)
    
    cte_sql += union_all_sql + ")"
    return cte_sql

# Example usage
csv_file_path = 'data.csv'
cte_sql = csv_to_cte_sql(csv_file_path)

# Generate JOIN conditions for each column
def generate_join_conditions(columns, other_table_alias='o'):
    """Generates join conditions for each column."""
    join_conditions = [f"c.{col} = {other_table_alias}.{col}" for col in columns]
    return ' AND '.join(join_conditions)

# Read the first chunk to get the column names
columns = pd.read_csv(csv_file_path, nrows=1).columns.tolist()
join_conditions = generate_join_conditions(columns)

# Example of using the CTE to join with another table and find non-matching rows
final_sql = f"""
{cte_sql}
SELECT c.*, o.*
FROM data_cte c
LEFT JOIN employees o ON {join_conditions}
WHERE o.id IS NULL
"""

print(final_sql)
