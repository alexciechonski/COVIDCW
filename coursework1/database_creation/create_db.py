"""
This script manages the creation and population of an SQLite database with COVID-19
restriction data. It includes functionality to create tables, insert data, and view
database structure, leveraging CSV data sources.

Classes:
    - DatabaseManager: Manages basic database operations such as creating tables,
      inserting data, deleting tables, and displaying database structure.
    - Tables: Extends the Frames class to manage specific database tables related to
      COVID-19 restriction data. It includes methods to create and populate tables
      like Date, Week, Restriction, Source, DailyRestriction, WeeklyRestriction,
      and SummaryRestriction.

Functions:
    - main(): Initializes the database and data tables, populates the database with
      data from CSV files, and displays the structure of the database.

Usage:
    Run this script as a standalone program to create the database structure, insert
    data from specified CSV files, and display the resulting tables in the database.
"""
from typing import Any
import sqlite3
from frames import Frames

class DatabaseManager:
    """
    Manages database operations such as creating tables, inserting data,
    and retrieving information about tables and fields.

    Attributes:
        _db (str): Path to the SQLite database.
        _conn (sqlite3.Connection): SQLite connection object.
    """
    def __init__(self, db_path: str) -> None:
        """
        Initializes the DatabaseManager with the path to the database.

        Parameters:
            db_path (str): Path to the SQLite database file.
        """
        self._db = db_path
        self._conn = sqlite3.connect(self._db)
        self._conn.execute("PRAGMA foreign_keys = ON;")

    def close_connection(self) -> None:
        """Closes the database connection."""
        if self._conn:
            self._conn.close()

    def show_tables(self) -> None:
        """
        Connects to an SQLite database and prints all table names.
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                print("Tables in the database:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("No tables found in the database.")
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

    def read_table_fields(self, table: str) -> None:
        """
        Connects to an SQLite database and prints all column names for a given table.

        Parameters:
            table: The name of the table to retrieve the fields from.
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            if columns:
                print(f"Fields in the table '{table}':")
                for column in columns:
                    print(f"- {column[1]} ({column[2]})")  # column[1] name, column[2] type
            else:
                print(f"No fields found or table '{table}' does not exist.")
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

    def read_table_vals(self, table: str) -> None:
        """
        Connects to an SQLite database and prints all the values in a given table.

        Parameters:
            table: The name of the table to retrieve the values from.
        """
        try:
            cursor = self._conn.cursor()
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
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

    def delete_table(self, table_name: str) -> None:
        """
        Deletes a specified table from the database.

        Parameters:
            table_name (str): The name of the table to delete.
        """
        cursor = self._conn.cursor()
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self._conn.commit()  # Commit the changes
            print(f"Table '{table_name}' has been deleted from the database '{self._db}'.")
        except sqlite3.DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")

    def insert_data(self, table_name: str, data: list[tuple[Any, ...]]) -> None:
        """
        Inserts data into an SQLite table.

        Parameters:
        - table_name (str): Name of the table to insert data into.
        - data (list of tuples): List of tuples, each tuple represents a row of data.
                                Example: [(1, '2023-01-01'), (2, '2023-01-02')]
        """
        cursor = self._conn.cursor()
        placeholders = ', '.join(['?' for _ in data[0]])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        try:
            for row in data:
                cursor.execute(insert_sql, row)
            print(f"Inserted {len(data)} rows into '{table_name}' successfully.")
            self._conn.commit()
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

    def create_table(self, table_name: str, cols_dict:dict[str,str]) -> None:
        """
        Creates a table in the database with specified columns.

        Parameters:
            table_name (str): Name of the table to create.
            cols_dict (dict): Column names as keys and data types as values.
        """
        cursor = self._conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cols_str = f"""
                    ({', '.join([f'{col_name} {constraint.upper()}' for col_name, constraint in cols_dict.items()])})
                    """
        query = f"CREATE TABLE {table_name} {cols_str}"
        try:
            cursor.execute(query)
            print(f"Table '{table_name}' created successfully.")
            self._conn.commit()
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

class Tables(Frames):
    """
    A subclass of Frames that manages creation of specific tables in the database
    and inserts data from various DataFrames.

    Attributes:
        db_path (str): Path to the SQLite database.
        daily_path (str): Path to the daily dataset CSV file.
        weekly_path (str): Path to the weekly dataset CSV file.
        summary_path (str): Path to the summary dataset CSV file.
    """
    def __init__(self, db_path: str, daily_path: str, weekly_path: str, summary_path: str) -> None:
        """
        Initializes the Tables class with database path and dataset paths.

        Parameters:
            db_path (str): Path to the SQLite database.
            daily_path (str): Path to the daily dataset CSV file.
            weekly_path (str): Path to the weekly dataset CSV file.
            summary_path (str): Path to the summary dataset CSV file.
        """
        super().__init__(daily_path=daily_path, weekly_path=weekly_path, summary_path=summary_path)
        self._db = db_path
        self.date_df = self.get_date_df()
        self.week_df = self.get_week_df()
        self.source_df = self.get_source_df()
        self.restriction_df = self.get_restriction_df()
        self.summary_restriction_df = self.get_summary_restriction_df()
        self.daily_restriction_df = self.get_daily_restriction_df()
        self.weekly_restriction_df = self.get_weekly_restriction_df()

    def t_date(self) -> None:
        """Creates and populates the 'Date' table with data from date_df."""
        manager = DatabaseManager(self._db)
        cols = {
            "date": "TEXT NOT NULL",
            "date_id":"INTEGER PRIMARY KEY",
        }
        manager.create_table("Date", cols)
        data = list(self.date_df.itertuples(index=False, name=None))
        manager.insert_data("Date", data)

    def t_week(self) -> None:
        """Creates and populates the 'Week' table with data from week_df."""
        manager = DatabaseManager(self._db)
        cols = {
            "week_start": "TEXT NOT NULL",
            "week_id":"INTEGER PRIMARY KEY",
        }
        manager.create_table("Week", cols)
        data = list(self.week_df.itertuples(index=False, name=None))
        manager.insert_data("Week", data)

    def t_restriction(self) -> None:
        """Creates and populates the 'Restriction' table with data from restriction_df."""
        manager = DatabaseManager(self._db)
        cols = {
            "restriction": "TEXT NOT NULL",
            "restriction_id":"INTEGER PRIMARY KEY",
        }
        manager.create_table("Restriction", cols)
        data = list(self.restriction_df.itertuples(index=False, name=None))
        manager.insert_data("Restriction", data)

    def t_source(self) -> None:
        """Creates and populates the 'Source' table with data from source_df."""
        manager = DatabaseManager(self._db)
        cols = {
            "source": "TEXT NOT NULL",
            "source_id":"INTEGER PRIMARY KEY",
        }
        manager.create_table("Source", cols)
        data = list(self.source_df.itertuples(index=False, name=None))
        manager.insert_data("Source", data)

    def t_daily_restriction(self) -> None:
        """
        Creates and populates the 'DailyRestriction' table with data
        from daily_restriction_df.
        """
        manager = DatabaseManager(self._db)
        cols = {
            "date_id": "INTEGER NOT NULL REFERENCES Date(date_id)",
            "restriction_id": "INTEGER NOT NULL REFERENCES Restriction(restriction_id)",
            "in_place": "INTEGER NOT NULL CHECK (in_place <= 1 AND in_place >= 0)"
        }
        manager.create_table("DailyRestriction", cols)
        data = list(self.daily_restriction_df.itertuples(index=False, name=None))
        manager.insert_data("DailyRestriction", data)

    def t_weekly_restriction(self) -> None:
        """
        Creates and populates the 'WeeklyRestriction' table with data
        from weekly_restriction_df.
        """
        manager = DatabaseManager(self._db)
        cols = {
            "week_id": "INTEGER NOT NULL REFERENCES Week(week_id)",
            "restriction_id": "INTEGER NOT NULL REFERENCES Restriction(restriction_id)",
            "in_place": "INTEGER NOT NULL CHECK (in_place <= 1 AND in_place >= 0)"
        }
        manager.create_table("WeeklyRestriction", cols)
        data = list(self.weekly_restriction_df.itertuples(index=False, name=None))
        manager.insert_data("WeeklyRestriction", data)

    def t_summary_restriction(self) -> None:
        """
        Creates and populates the 'SummaryRestriction' table with data
        from summary_restriction_df.
        """
        manager = DatabaseManager(self._db)
        cols = {
            "date_id": "INTEGER NOT NULL REFERENCES Date(date_id)",
            "restriction_id": "INTEGER NOT NULL REFERENCES Restriction(restriction_id)",
            "source_id": "INTEGER NOT NULL REFERENCES Source(source_id)",
            "in_place": "INTEGER NOT NULL CHECK (in_place <= 1 AND in_place >= 0)"
        }
        manager.create_table("SummaryRestriction", cols)
        data = list(self.summary_restriction_df.itertuples(index=False, name=None))
        manager.insert_data("SummaryRestriction", data)

    def generate(self) -> None:
        """
        Calls methods to create and populate all tables in the database
        based on the data provided in the DataFrames.
        """
        self.t_date()
        self.t_week()
        self.t_restriction()
        self.t_source()
        self.t_daily_restriction()
        self.t_weekly_restriction()
        self.t_summary_restriction()


def main() -> None:
    """Creates and populates the database based on the ERD"""
    db_path = "coursework1/database_creation/covid2.db" #integrity error
    daily_path = "coursework1/datasets/restrictions_daily.csv"
    weekly_path = "coursework1/datasets/restrictions_weekly.csv"
    summary_path = "coursework1/datasets/restrictions_summary.csv"
    manager = DatabaseManager(db_path)
    tables = Tables(
        db_path,
        daily_path=daily_path,
        weekly_path=weekly_path,
        summary_path=summary_path
        )
    try:
        tables.generate()
        manager.show_tables()
    finally:
        manager.close_connection()

if __name__ == "__main__":
    main()
