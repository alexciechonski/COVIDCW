import sqlite3
import pandas as pd

def create_table(database_path, table_name, fields, primary_keys):
    """
    Creates a table in an SQLite database.
    
    Parameters:
    - database_path: The name of the SQLite database file.
    - table_name: The name of the table to be created.
    - fields: A dictionary where the keys are column names and the values are the column types (e.g., {"id": "INTEGER", "name": "TEXT"}).
    - primary_keys: A list of column names to be used as primary keys.
    
    Example:
    create_table('mydb.db', 'users', {'id': 'INTEGER', 'name': 'TEXT', 'email': 'TEXT'}, ['id'])
    """
    
    # Generate field definitions as a list of strings
    field_definitions = [f"{field} {data_type}" for field, data_type in fields.items()]
    
    # Generate primary key constraint
    primary_key_definition = f", PRIMARY KEY({', '.join(primary_keys)})" if primary_keys else ""
    
    # Combine field definitions and primary key into the CREATE TABLE statement
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(field_definitions)}
        {primary_key_definition}
    );
    """
    
    # Connect to the database and execute the query
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def create_daily(database_path):
    daily_fields = {
        'date_days':'TEXT',
        'schools_closed':"INTEGER",
        "shops_closed": "INTEGER",
        "eating_places_closed":"INTEGER",
        "stay_at_home": "INTEGER",
        "household_mixing_indoors_banned":"INTEGER",
        "wfh":"INTEGER",
        "rule_of_6_indoors":"INTEGER",
        "curfew":"INTEGER",
        "eat_out_help_out":"INTEGER"
    }
    daily_primary = ['date_days']
    create_table(database_path, 'Daily', daily_fields, daily_primary)

def create_weekly(database_path):
    weekly_fields = {
        'date_weeks':'TEXT',
        'schools_closed':"INTEGER",
        "pubs_closed": "INTEGER",
        "shops_closed": "INTEGER",
        "eating_places_closed":"INTEGER",
        "stay_at_home": "INTEGER",
        "household_mixing_indoors_banned":"INTEGER",
        "wfh":"INTEGER",
        "rule_of_6_indoors":"INTEGER",
        "curfew":"INTEGER",
        "eat_out_help_out":"INTEGER"
    }
    weekly_primary = ['date_weeks']
    create_table(database_path, 'Weekly', weekly_fields, weekly_primary)

def create_summary(database_path):
    summary_fields = {
        'date':'TEXT',
        'restriction':"TEXT",
        "source": "TEXT",
        'schools_closed':"INTEGER",
        "pubs_closed": "INTEGER",
        "shops_closed":"INTEGER",
        "eating_places_closed":"INTEGER",
        "stay_at_home": "INTEGER",
        "household_mixing_indoors_banned":"INTEGER",
        "wfh":"INTEGER",
        "rule_of_6_indoors":"INTEGER",
        "curfew":"INTEGER",
        "eat_out_help_out":"INTEGER"
    }
    summary_primary = ['date']
    create_table(database_path, 'Summary', summary_fields, summary_primary)

def show_tables(database_path):
    """
    Connects to an SQLite database and prints all table names.

    Parameters:
    - database_path: The name of the SQLite database file (e.g., 'mydatabase.db').
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Execute the query to retrieve all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        # Fetch all results (table names)
        tables = cursor.fetchall()

        # Check if any tables were found
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in the database.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

def read_table_fields(database_path, table):
    """
    Connects to an SQLite database and prints all column names for a given table.

    Parameters:
    - database_path: The path to the SQLite database file (e.g., 'mydatabase.db').
    - table: The name of the table to retrieve the fields from.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Execute the query to get column information for the specified table
        cursor.execute(f"PRAGMA table_info({table});")

        # Fetch all column details
        columns = cursor.fetchall()

        # Check if columns were found
        if columns:
            print(f"Fields in the table '{table}':")
            for column in columns:
                print(f"- {column[1]} ({column[2]})")  # column[1] is the name, column[2] is the type
        else:
            print(f"No fields found or table '{table}' does not exist.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

def read_table_vals(database_path, table):
    """
    Connects to an SQLite database and prints all the values in a given table.

    Parameters:
    - database_path: The path to the SQLite database file (e.g., 'mydatabase.db').
    - table: The name of the table to retrieve the values from.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Execute a query to select all values from the specified table
        cursor.execute(f"SELECT * FROM {table}")

        # Fetch all rows from the table
        rows = cursor.fetchall()

        # Get column names for better readability
        column_names = [description[0] for description in cursor.description]

        # Check if the table contains any rows
        if rows:
            print(f"Values in the table '{table}':")
            # Print column names
            print(f"{' | '.join(column_names)}")

            # Print each row of values
            for row in rows:
                print(row)
        else:
            print(f"The table '{table}' is empty or does not exist.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

def dataframe_to_sql(df: pd.DataFrame, db_name: str, table_name: str):
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_name)
    
    try:
        # Write the DataFrame to the SQLite table
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"DataFrame successfully written to {table_name} table in {db_name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        conn.close()

def delete_table(db_name: str, table_name: str):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Delete the table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()  # Commit the changes
        print(f"Table '{table_name}' has been deleted from the database '{db_name}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        conn.close()

def main():
    DB = "database.db"
    show_tables(DB)
    delete_table(DB, "Daily")
    delete_table(DB, "Weekly")
    delete_table(DB, "Summary")
    delete_table(DB, "daily2")
    show_tables(DB)


if __name__ == "__main__":
    main()