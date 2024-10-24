import sqlite3
import pandas as pd

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
    except sqlite3.DatabaseError as db_err:
        print(f"Database error occurred: {db_err}")
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
    except sqlite3.DatabaseError as db_err:
        print(f"Database error occurred: {db_err}")
    finally:
        # Close the connection
        conn.close()

def main():
    DB = "database.db"
    daily = pd.read_csv("restrictions_daily.csv")
    weekly = pd.read_csv("restrictions_weekly.csv")
    summary = pd.read_csv("restrictions_weekly.csv")
    dataframe_to_sql(daily, DB, "Daily")
    dataframe_to_sql(weekly, DB, "Weekly")
    dataframe_to_sql(summary, DB, "Summary")
    show_tables(DB)
    read_table_fields(DB, "Daily")
    read_table_fields(DB, "Weekly")
    read_table_fields(DB, "Summary")


if __name__ == "__main__":
    main()