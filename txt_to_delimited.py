def text_to_sql_in_clause(file_path):
    # Read lines from the file and strip any whitespace characters
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    # Convert lines into a delimited string suitable for SQL IN clause
    in_clause = "', '".join(lines)
    sql_in_statement = f"'{in_clause}'"

    return sql_in_statement

# Example usage
file_path = 'input.txt'
sql_in_clause = text_to_sql_in_clause(file_path)
print(f"IN ({sql_in_clause})")
