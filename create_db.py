import sqlite3

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
        'schools_closed':"BOOL",
        "shops_closed": "BOOL",
        "eating_places_closed":"BOOL",
        "stay_at_home": "BOOL",
        "household_mixing_indoors_banned":"BOOL",
        "wfh":"BOOL",
        "rule_of_6_indoors":"BOOL",
        "curfew":"BOOL",
        "eat_out_help_out":"BOOL"
    }
    daily_primary = ['date_days']
    create_table(database_path, 'Daily', daily_fields, daily_primary)

def create_weekly(database_path):
    weekly_fields = {
        'date_weeks':'TEXT',
        'schools_closed':"BOOL",
        "pubs_closed": "BOOL",
        "shops_closed": "BOOL",
        "eating_places_closed":"BOOL",
        "stay_at_home": "BOOL",
        "household_mixing_indoors_banned":"BOOL",
        "wfh":"BOOL",
        "rule_of_6_indoors":"BOOL",
        "curfew":"BOOL",
        "eat_out_help_out":"BOOL"
    }
    weekly_primary = ['date_weeks']
    create_table(database_path, 'Weekly', weekly_fields, weekly_primary)

def create_summary(database_path):
    summary_fields = {
        'date':'TEXT',
        'restriction':"TEXT",
        "source": "TEXT",
        'schools_closed':"BOOL",
        "pubs_closed": "BOOL",
        "shops_closed":"BOOL",
        "eating_places_closed":"BOOL",
        "stay_at_home": "BOOL",
        "household_mixing_indoors_banned":"BOOL",
        "wfh":"BOOL",
        "rule_of_6_indoors":"BOOL",
        "curfew":"BOOL",
        "eat_out_help_out":"BOOL"
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
    pass


def main():
    DB = "database.db"
    # create_daily(DB)
    # create_weekly(DB)
    # create_summary(DB)

    show_tables(DB)
    read_table_fields(DB,"Daily")

if __name__ == "__main__":
    main()