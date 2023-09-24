import pandas as pd
import os
import chardet
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Define a function to detect encoding of a file

def transform_iso_code(code):
    # Add your own mapping from ISO 3166 codes to actual names here
    mapping = {
        'US': 'United States',
        'CA': 'Canada',
        'GB': 'United Kingdom',
        'AE': 'United Arab Emirates',
        'AUS': 'Australia',
        'BR': 'Brazil',
        'CAN': 'Canada',
        'CN': 'China',
        'DE': 'Germany',
        'FR': 'France',
        'HKG': 'Hong Kong',
        'IN': 'India',
        'HN': 'Honduras',
        'JP': 'Japan',
        'HU': 'Hungary',
        'NZ': 'New Zealand',
        'NL': 'Netherlands',
        'MX': 'Mexico',
        'GR': 'Greece',
        'ES': 'Spain',
        'PT': 'Portugal',
        'HR': 'Croatia',
        'NG': 'Nigeria',
        'SG': 'Singapore',
        'IT': 'Italy',
        'RU': 'Russian',  # Corrected ISO code
        'MT': 'Malta',
        'PK': 'Pakistan',
        'MKD': 'North Macedonia',
        'TR': 'Türkiye',
        'GE': 'Greenland',
    }

    return mapping.get(code, 'Unknown')
# Rest of the code remains the same...

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())

    detected_encoding = result['encoding']
    confidence = result['confidence']

    if detected_encoding is None:
        print("Encoding detection failed. Could not determine the encoding.")
    else:
        print(f"Detected encoding: {detected_encoding} with confidence: {confidence}")

    return detected_encoding


# Define a function to apply transformations to the DataFrame
def apply_transformations(df):
    # Transformation: Replace 'L', 'M', 'S' with 'large', 'medium', 'small'
    df['company_size'] = df['company_size'].replace({'L': 'large', 'M': 'medium', 'S': 'small'})

    # Transformation: Replace 'PT' with 'part time' and 'FT' with 'full time'
    df['employment_type'] = df['employment_type'].replace(
        dict(PT='part time', FT='full time', FL='full time', CT='Contract'))

    # Elaborating experience levels
    df['experience_level'] = df['experience_level'].replace(
        {'EN': 'Entry-level', 'MI': 'Middle-level', 'SE': "Senior-level", 'EX': 'Executive-level'})

    # Applying transformation for 'company_location' based on ISO code
    df['company_location'] = df['company_location'].apply(transform_iso_code)

    return df


# Define a function to load and display the first n rows of a CSV file
def load_and_display_csv(csv_file_path, n=4):
    try:
        # Detect encoding
        encoding = detect_encoding(csv_file_path)

        # Attempt to read the CSV file with the detected encoding
        df = pd.read_csv(csv_file_path, encoding=encoding)

        # Drop rows with any invalid values
        df.dropna(inplace=True)

        # Remove duplicate entries based on all columns
        df.drop_duplicates(inplace=True)

        # Display the first n rows
        print(f"Processed CSV - First {n} rows:")
        print(df.head(n))

        # Save the processed data to a new CSV file
        processed_file_path = csv_file_path.replace('.csv', '_processed.csv')
        df.to_csv(processed_file_path, index=False)
        print(f"Processed data saved to: {processed_file_path}")

        return df

    except pd.errors.ParserError as e:
        print("Error reading CSV. Please check the file for invalid data or format.")
        return None
    except FileNotFoundError:
        print(f"CSV file not found at: {csv_file_path}")
        return None


# Define a function to insert DataFrame into the database
def insert_dataframe_into_db(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print("Data loaded into the database.")


# Define a function to fetch data from the database
def fetch_data_from_db(engine, table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, con=engine)
        return df
    except Exception as e:
        print("Error fetching data from the database:", str(e))
        return None
    finally:
        engine.dispose()

# Define a function to create a bar plot for company sizes
def create_company_size_country_location_plot(df):
    if df is not None and 'company_size' in df and 'company_location' in df:
        plt.figure(figsize=(12, 8))
        grouped_data = df.groupby(['company_location', 'company_size']).size().unstack()
        grouped_data.plot(kind='bar', stacked=True, colormap='viridis')
        plt.title('Company Size Distribution by Country')
        plt.xlabel('Country')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend(title='Company Size', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
    else:
        print("Dataframe is empty or does not contain necessary columns ('company_size', 'company_location').")


def create_country_salary_plot(df):
    if df is not None and 'company_location' in df and 'salary_in_usd' in df:
        plt.figure(figsize=(13, 9))
        ax = df.groupby('company_location')['salary_in_usd'].mean().plot(kind='bar', color='skyblue')
        plt.title('Average Salary by Country')
        plt.xlabel('Country')
        plt.ylabel('Average Salary')
        plt.xticks(rotation=45, ha='right')  # Adjusted x-axis label rotation and alignment
        plt.tight_layout()
        plt.show()
    else:
        print("Dataframe is empty or does not contain necessary columns ('company_location', 'salary_in_usd').")


def create_experience_salary_plot(df):
    if df is not None and 'company_location' in df and 'salary_in_usd' in df and 'experience_level' in df:
        plt.figure(figsize=(14, 9))
        df_grouped = df.groupby(['company_location', 'experience_level'])['salary_in_usd'].mean().unstack()
        ax = df_grouped.plot(kind='bar', stacked=True, colormap='viridis')
        plt.title('Average Salary by Country and Experience')
        plt.xlabel('Country')
        plt.ylabel('Average Salary')
        plt.xticks(rotation=45, ha='right')  # Adjusted x-axis label rotation and alignment
        plt.tight_layout()
        plt.legend(title='Experience', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
    else:
        print("Dataframe is empty or does not contain necessary columns ('company_location', 'salary_in_usd', 'experience').")


def create_company_size_experience_plot(df):
    if df is not None and 'company_size' in df and 'salary_in_usd' in df and 'experience_level' in df:
        plt.figure(figsize=(13, 9))
        df_grouped = df.groupby(['company_size', 'experience_level'])['salary_in_usd'].mean().unstack()
        ax = df_grouped.plot(kind='bar', colormap='viridis')
        plt.title('Average Salary by Company Size and Experience')
        plt.xlabel('Company Size')
        plt.ylabel('Average Salary')
        plt.xticks(rotation=45, ha='right')  # Adjusted x-axis label rotation and alignment
        plt.tight_layout()
        plt.legend(title='Experience', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
    else:
        print("Dataframe is empty or does not contain necessary columns.")

# Main function
def main():
    # Specify the CSV file path
    csv_file_path = './ds_salaries.csv'

    # Load CSV file and display
    df = load_and_display_csv(csv_file_path)

    if df is not None:
        # Apply transformations
        df_transformed = apply_transformations(df)

        # Specify the database URL
        db_path = 'sqlite:///your_database.db'
        engine = create_engine(db_path)

        # Insert DataFrame into the database
        table_name = 'your_table_name'  # Replace with your table name
        insert_dataframe_into_db(df_transformed, table_name, engine)

        # Fetch data from the database
        df_from_db = fetch_data_from_db(engine, table_name)

        if df_from_db is not None:
            # Create a bar plot for company sizes
            create_country_salary_plot(df)
            create_experience_salary_plot(df)
            create_company_size_experience_plot(df)

if __name__ == "__main__":
    main()
