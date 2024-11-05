import sqlite3
import pandas as pd
from frames import Frames

class DatabaseCreation:
    def __init__(self, db) -> None:
        self.db = db

    def show_tables(self):
        """
        Connects to an SQLite database and prints all table names.
        """
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db)
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

    def read_table_fields(self, table: str):
        """
        Connects to an SQLite database and prints all column names for a given table.

        Parameters:
        - table: The name of the table to retrieve the fields from.
        """
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db)
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

    def read_table_vals(self, table: str):
        """
        Connects to an SQLite database and prints all the values in a given table.

        Parameters:
        - table: The name of the table to retrieve the values from.
        """
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db)
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

    def delete_table(self, table_name: str):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        try:
            # Delete the table if it exists
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()  # Commit the changes
            print(f"Table '{table_name}' has been deleted from the database '{self.db}'.")
        except sqlite3.DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
        finally:
            # Close the connection
            conn.close()

    def create_table(self, table_name, columns, foreign_keys=None, primary_key=None):
        """
        Creates a table in SQLite.

        Parameters:
        - table_name (str): Name of the table to create.
        - columns (list of tuples): Each tuple should contain the column name, data type, and constraints.
                                Example: [("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"), 
                                            ("name", "TEXT", "NOT NULL"), 
                                            ("age", "INTEGER", "DEFAULT 0")]
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON;")

        columns_definition = ", ".join([f"{col[0]} {col[1]} {col[2]}" for col in columns])
        
        foreign_keys_definition = ""
        if foreign_keys:
            foreign_keys_definition = ", " + ", ".join(
                [f"FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]}" for fk in foreign_keys]
            )

        primary_key_definition = ""
        if primary_key:
            primary_key_definition = f", PRIMARY KEY ({', '.join(primary_key)})"

        create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {columns_definition}
                    {foreign_keys_definition}
                    {primary_key_definition}
                );
                """        
        try:
            # Execute the SQL statement
            cursor.execute(create_table_sql)
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # Commit changes and close the connection
            conn.commit()
            conn.close()

    def insert_data(self, table_name, data):
        """
        Inserts data into an SQLite table.

        Parameters:
        - table_name (str): Name of the table to insert data into.
        - data (list of tuples): List of tuples, where each tuple represents a row of data to insert.
                                Example: [(1, '2023-01-01'), (2, '2023-01-02')]
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        # Generate placeholders for the data based on the number of columns
        placeholders = ', '.join(['?' for _ in data[0]])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        try:
            # Execute the insert statement for all rows in data
            for t in data:
                cursor.execute(insert_sql, t)
            # print(f"Inserted {len(data)} rows into '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # Commit changes and close the connection
            print('dun')
            conn.commit()
            conn.close()
            
def put_data(db_path, df, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    data = list(df.itertuples(index=False, name=None))
    print(data)
    # Generate placeholders based on the number of columns in the DataFrame
    placeholders = ', '.join(['?' for _ in range(len(df.columns))])
    insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
    print(insert_sql)
    
    try:
        # Execute the insert statement for all rows in data
        cursor.executemany(insert_sql, data)
        print(f"Inserted {len(data)} rows into '{table_name}' table.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Commit changes and close the connection
        conn.commit()
        conn.close()

def make_table(db_path, table_name, cols_dict:dict):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cols_str = f"({', '.join([f'{col_name} {constraint.upper()}' for col_name, constraint in cols_dict.items()])})"
    query = f"CREATE TABLE {table_name} {cols_str}"
    try:
        cursor.execute(query)
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.commit()
        conn.close()

class Tables(Frames):
    def __init__(self, db_path: str, daily_path: str, weekly_path: str, summary_path: str) -> None:
        super().__init__(daily_path=daily_path, weekly_path=weekly_path, summary_path=summary_path)
        self.db = db_path
        self.date_df = self.get_date_df()
        self.week_df = self.get_week_df()
        self.source_df = self.get_source_df()
        self.restriction_df = self.get_restriction_df()
        self.summary_restriction_df = self.get_summary_restriction_df()
        self.daily_restriction_df = self.get_daily_restriction_df()
        self.weekly_restriction_df = self.get_weekly_restriction_df()

    def t_date(self):
        db = DatabaseCreation(self.db)
        cols = {
            "date": "TEXT",
            "date_id":"INTEGER PRIMARY KEY",
        }
        make_table(self.db, "Date8", cols)
        data = list(self.date_df.itertuples(index=False, name=None))
        db.insert_data("Date8", data)

    def week(db_path, weekly_df):
        db = DatabaseCreation(db_path)
        week_cols = [
            ("week_id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"),
            ("week_start", "INTEGER", "NOT NULL")
        ]
        db.create_table("Week", week_cols)


    def restriction(db_path, summary):
        db = DatabaseCreation(db_path)
        restriction_cols = [
            ("restriction_id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"),
            ("name", "TEXT", "NOT NULL")
        ]
        db.create_table("Restriction", restriction_cols)

    def source(db_path, summary):
        db = DatabaseCreation(db_path)
        source_cols = [
            ("source_id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"),
            ("name", "TEXT", "NOT NULL")
        ]
        db.create_table("Source", source_cols)

    def daily_restriction(db_path, daily, summary):
        db = DatabaseCreation(db_path)
        columns = [
            ("value", "INTEGER", "NOT NULL"),
            ("date_id", "INTEGER", "NOT NULL"),
            ("restriction_id", "INTEGER", "NOT NULL")
            ]
        foreign_keys = [
                ("date_id", "Date(date_id)"),
                ("restriction_id", "Restriction(restriction_id)")
            ]
        db.create_table("DailyRestrictions", columns, foreign_keys=foreign_keys)


def main():
    DB = "database_creation/covid.db"
    daily_path = "datasets/restrictions_daily.csv"
    weekly_path = "datasets/restrictions_weekly.csv"
    summary_path = "datasets/restrictions_summary.csv"
    t = Tables(DB, daily_path=daily_path, weekly_path=weekly_path, summary_path=summary_path)
    # t.t_date()

    # data = list(t.date_df.itertuples(index=False, name=None))
    # print(type(data[0][0]))
    # # Generate placeholders based on the number of columns in the DataFrame
    # placeholders = ', '.join(['?' for _ in range(len(t.date_df.columns))])
    # table_name = "Test"
    # insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
    # print(insert_sql)
    



    db = DatabaseCreation(DB)
    db.show_tables()
    db.read_table_vals("Date8")
    


if __name__ == "__main__":
    main()