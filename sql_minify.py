import re

def minify_sql(sql_code):
    # Remove multi-line comments
    sql_code = re.sub(r'/\*.*?\*/', '', sql_code, flags=re.DOTALL)
    
    # Remove single-line comments
    sql_code = re.sub(r'--.*', '', sql_code)
    
    # Remove leading and trailing whitespace from each line
    sql_code = '\n'.join([line.strip() for line in sql_code.splitlines()])
    
    # Remove blank lines
    sql_code = '\n'.join([line for line in sql_code.splitlines() if line.strip() != ''])
    
    # Replace multiple spaces with a single space
    sql_code = re.sub(r'\s+', ' ', sql_code)
    
    return sql_code.strip()

# Paste your SQL code here between the triple quotes
sql_code = """

"""

# Minify the SQL code
minified_sql = minify_sql(sql_code)
print(minified_sql)
