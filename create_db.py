import sqlite3

def create_table(db_name, table_name, fields, primary_keys):
    """
    Creates a table in an SQLite database.
    
    Parameters:
    - db_name: The name of the SQLite database file.
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
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def main():
    DB = "database.db"
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

    create_table(DB, 'Daily', {})

if __name__ == "__main__":
    main()