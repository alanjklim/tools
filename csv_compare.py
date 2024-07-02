import pandas as pd

def compare_and_union_csv(file1, file2, output_file):
    # Read the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Ensure the columns are the same
    if set(df1.columns) != set(df2.columns):
        raise ValueError("The columns in the two CSV files do not match.")
    
    # Reorder columns of df2 to match df1
    df2 = df2[df1.columns]
    
    # Create a column to track the origin of the data
    df1['database'] = 'source'
    df2['database'] = 'destination'
    
    # Reorder to place 'database' as the first column
    columns = ['database'] + df1.columns[:-1].tolist() + ['differences']
    
    # Initialize a list to hold the result rows
    result = []
    
    # Find all unique ids assuming the first column is the unique identifier
    all_ids = set(df1.iloc[:, 0]).union(set(df2.iloc[:, 0]))

    for unique_id in all_ids:
        source_row = df1[df1.iloc[:, 0] == unique_id]
        dest_row = df2[df2.iloc[:, 0] == unique_id]
        
        if not source_row.empty and not dest_row.empty:
            source_row = source_row.iloc[0]
            dest_row = dest_row.iloc[0]
            differences = []
            for col in df1.columns:
                if col != 'database':
                    if pd.api.types.is_numeric_dtype(df1[col]) and pd.api.types.is_numeric_dtype(df2[col]):
                        if source_row[col] != dest_row[col]:
                            differences.append(col)
                    elif pd.api.types.is_datetime64_any_dtype(df1[col]) and pd.api.types.is_datetime64_any_dtype(df2[col]):
                        if pd.to_datetime(source_row[col]) != pd.to_datetime(dest_row[col]):
                            differences.append(col)
                    else:
                        if str(source_row[col]) != str(dest_row[col]):
                            differences.append(col)
            differences_str = ", ".join(differences)
            
            source_row = source_row.to_frame().T
            dest_row = dest_row.to_frame().T
            source_row['differences'] = differences_str
            dest_row['differences'] = differences_str
            
            result.append(source_row)
            result.append(dest_row)
        elif not source_row.empty:
            source_row = source_row.iloc[0]
            source_row = source_row.to_frame().T
            source_row['differences'] = "Row missing in destination"
            result.append(source_row)
        elif not dest_row.empty:
            dest_row = dest_row.iloc[0]
            dest_row = dest_row.to_frame().T
            dest_row['differences'] = "Row missing in source"
            result.append(dest_row)
    
    # Concatenate all result rows into a single DataFrame
    result_df = pd.concat(result).reset_index(drop=True)
    result_df = result_df[columns]
    
    # Save the result to a CSV file
    result_df.to_csv(output_file, index=False)

# Example usage
# Update these file paths to match your actual CSV files
file1 = 'source_data.csv'
file2 = 'destination_data.csv'
output_file = 'comparison_result.csv'

compare_and_union_csv(file1, file2, output_file)

print(f"Comparison result saved to {output_file}")
