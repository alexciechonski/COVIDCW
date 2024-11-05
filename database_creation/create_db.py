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
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
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
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
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
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            if rows:
                print(f"Values in the table '{table}':")
                print(f"{' | '.join(column_names)}")
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
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()  # Commit the changes
            print(f"Table '{table_name}' has been deleted from the database '{self.db}'.")
        except sqlite3.DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
        finally:
            conn.close()

    def insert_data(self, table_name, data):
        """
        Inserts data into an SQLite table.

        Parameters:
        - table_name (str): Name of the table to insert data into.
        - data (list of tuples): List of tuples, where each tuple represents a row of data to insert.
                                Example: [(1, '2023-01-01'), (2, '2023-01-02')]
        """
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        placeholders = ', '.join(['?' for _ in data[0]])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        try:
            for t in data:
                cursor.execute(insert_sql, t)
            print(f"Inserted {len(data)} rows into '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.commit()
            conn.close()
            
    def create_table(self, table_name, cols_dict:dict):
        conn = sqlite3.connect(self.db)
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
            "date": "TEXT NOT NULL",
            "date_id":"INTEGER PRIMARY KEY",
        }
        db.create_table("Date", cols)
        data = list(self.date_df.itertuples(index=False, name=None))
        db.insert_data("Date", data)

    def t_week(self):
        db = DatabaseCreation(self.db)
        cols = {
            "week_start": "TEXT NOT NULL",
            "week_id":"INTEGER PRIMARY KEY",
        }
        db.create_table("Week", cols)
        data = list(self.week_df.itertuples(index=False, name=None))
        db.insert_data("Week", data)

    def t_restriction(self):
        db = DatabaseCreation(self.db)
        cols = {
            "restriction": "TEXT NOT NULL",
            "restriction_id":"INTEGER PRIMARY KEY",
        }
        db.create_table("Restriction", cols)
        data = list(self.restriction_df.itertuples(index=False, name=None))
        db.insert_data("Restriction", data)

    def t_source(self):
        db = DatabaseCreation(self.db)
        cols = {
            "source": "TEXT NOT NULL",
            "source_id":"INTEGER PRIMARY KEY",
        }
        db.create_table("Source", cols)
        data = list(self.source_df.itertuples(index=False, name=None))
        db.insert_data("Source", data)

    def t_daily_restriction(self):
        db = DatabaseCreation(self.db)
        cols = {
            "date_id": "INTEGER NOT NULL REFERENCES Date(date_id)", 
            "restriction_id": "INTEGER NOT NULL REFERENCES Restriction(restriction_id)",  
            "in_place": "INTEGER NOT NULL CHECK (in_place <= 1 AND in_place >= 0)"  
        }
        db.create_table("DailyRestriction", cols)
        data = list(self.daily_restriction_df.itertuples(index=False, name=None))
        db.insert_data("DailyRestriction", data)

    def t_weekly_restriction(self):
        db = DatabaseCreation(self.db)
        cols = {
            "week_id": "INTEGER NOT NULL REFERENCES Week(week_id)",  
            "restriction_id": "INTEGER NOT NULL REFERENCES Restriction(restriction_id)",  
            "in_place": "INTEGER NOT NULL CHECK (in_place <= 1 AND in_place >= 0)"  
        }
        db.create_table("WeeklyRestriction", cols)
        data = list(self.weekly_restriction_df.itertuples(index=False, name=None))
        db.insert_data("WeeklyRestriction", data)

    def t_summary_restriction(self):
        db = DatabaseCreation(self.db)
        cols = {
            "date_id": "INTEGER NOT NULL REFERENCES Date(date_id)", 
            "restriction_id": "INTEGER NOT NULL REFERENCES Restriction(restriction_id)",
            "source_id": "INTEGER NOT NULL REFERENCES Source(source_id)",  
            "in_place": "INTEGER NOT NULL CHECK (in_place <= 1 AND in_place >= 0)"  
        }
        db.create_table("SummaryRestriction", cols)
        data = list(self.summary_restriction_df.itertuples(index=False, name=None))
        db.insert_data("SummaryRestriction", data)

    def generate(self):
        self.t_date()
        self.t_week()
        self.t_restriction()
        self.t_source()
        self.t_daily_restriction()
        self.t_weekly_restriction()
        self.t_summary_restriction()


def main():
    DB = "database_creation/covid.db"
    daily_path = "datasets/restrictions_daily.csv"
    weekly_path = "datasets/restrictions_weekly.csv"
    summary_path = "datasets/restrictions_summary.csv"
    db = DatabaseCreation(DB)
    tables = Tables(DB, daily_path=daily_path, weekly_path=weekly_path, summary_path=summary_path)
    tables.generate()
    db.show_tables()
    

if __name__ == "__main__":
    main()