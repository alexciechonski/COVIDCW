import pytest
from sql_queries import Queries
from ..coursework1.data_exploration.main import DataPreparation, DataLoader  
import sqlite3  

DB = "coursework2/sql_queries.py"
TXT_FILE = "queries.txt"
QUERIES = Queries.get_queries(TXT_FILE)

def assert_empty(query):
    """Assert that the query result is empty."""
    que = Queries(DB, TXT_FILE)
    res = que.select_query(query)
    assert res == [], f"Expected empty result, got {res}"

def check_presence(data, table):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        placeholder = " AND ".join([f"column{i+1} = ?" for i in range(len(data[0]))])
        query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {placeholder})"
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            print("Query successful")
        except sqlite3.DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
    assert results == []

class Query1:
    def test_select1():
        return assert_empty(QUERIES[0])

    def test_validate1():
        data_loader = DataLoader(
        "coursework1/datasets/restrictions_daily.csv",
        "coursework1/datasets/restrictions_weekly.csv",
        "coursework1/datasets/restrictions_summary.csv"
        )
        daily, weekly, summary = data_loader.load_data()
        prep = DataPreparation(daily, weekly, summary)
        timeline_data = prep.cumulative_timeline_data(daily)
        que = Queries(DB, TXT_FILE)
        assert timeline_data == que.select_query(QUERIES[0])

class Query2:
    def test_insertion2():
        pass

    def duplicate_test2():
        pass

class Query3:
    def test_presence3(deleted_row):
        que = Queries(DB, TXT_FILE)
        que.mod_query(QUERIES[2])
        return check_presence(deleted_row, 'Date')

    def check_for_presence3():
        # try deleting if not present
        pass

class Query4:
    def check_for_presence_after_update4():
        pass

    def check_not_existent4():
        pass

class Query5:
    def check_no_match5():
        pass

    def empty5():
        return assert_empty(QUERIES[4])

class Query6:
    def empty6():
        return assert_empty(QUERIES[5])

    def validate6():
        pass
