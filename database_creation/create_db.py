import sqlite3
import pandas as pd

class DatabaseCreation:
    def show_tables(self, database_path: str):
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

    def read_table_fields(self, database_path: str, table: str):
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

    def read_table_vals(self, database_path: str, table: str):
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

    def dataframe_to_sql(self, df: pd.DataFrame, db_name: str, table_name: str, not_null_columns:list=None, default_values:dict=None, check_constraints:dict=None):
        """
        Writes a DataFrame to a SQLite table with specified constraints.

        Parameters:
            df (pd.DataFrame): DataFrame to write to the SQLite database.
            db_name (str): Name of the SQLite database file.
            table_name (str): Name of the table to write data into.
            not_null_columns (list): List of columns to set as NOT NULL.
            default_values (dict): Dictionary with columns as keys and their default values as values.
            check_constraints (dict): Dictionary with columns as keys and SQL check constraints as values.
        """
        # Create a connection to the SQLite database
        conn = sqlite3.connect(db_name)
        
        try:
            # Write the DataFrame to the SQLite table
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            cursor = conn.cursor()
            
            # Get the current schema of the table
            cursor.execute(f"PRAGMA table_info({table_name})")

            # Prepare the constraints
            alterations = []
            
            if not_null_columns:
                for column in not_null_columns:
                    if column in df.columns:
                        alterations.append(f"ALTER TABLE {table_name} ALTER COLUMN {column} SET NOT NULL")
            
            if default_values:
                for column, default in default_values.items():
                    if column in df.columns:
                        alterations.append(f"ALTER TABLE {table_name} ALTER COLUMN {column} SET DEFAULT {default}")
            
            if check_constraints:
                for column, check in check_constraints.items():
                    if column in df.columns:
                        alterations.append(f"ALTER TABLE {table_name} ADD CHECK ({check})")
            
            for alter in alterations:
                try:
                    cursor.execute(alter)
                except sqlite3.DatabaseError as e:
                    print(f"Error applying alteration '{alter}': {e}")
            
            conn.commit()
            print(f"DataFrame successfully written to {table_name} table in {db_name} with constraints applied.")
        
        except sqlite3.DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
        finally:
            conn.close()

    def delete_table(self, db_name: str, table_name: str):
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
    daily = pd.read_csv("datasets/restrictions_daily.csv")
    weekly = pd.read_csv("datasets/restrictions_weekly.csv")
    summary = pd.read_csv("datasets/restrictions_weekly.csv")
    db = DatabaseCreation()
    db.dataframe_to_sql(daily, DB, "Daily")
    db.dataframe_to_sql(weekly, DB, "Weekly")
    db.dataframe_to_sql(summary, DB, "Summary")
    db.show_tables(DB)
    db.read_table_fields(DB, "DailyTEST")
    db.read_table_fields(DB, "Weekly")
    db.read_table_fields(DB, "Summary")


if __name__ == "__main__":
    main()