import pytest
from coursework2.sql_queries import Queries
import sqlite3  
import re
from ..coursework1.database_creation.create_db import Tables
from ..coursework1.database_creation.frames import Frames
import coursework1
import pandas as pd

# DB = "empty.db"
DB = "coursework2/covid_copy.db"
TXT_FILE = "coursework2/queries.txt"
QUERIES = Queries.get_queries(TXT_FILE)

def assert_empty(query):
    """Assert that the query result is empty."""
    que = Queries(DB, TXT_FILE)
    res = que.select_query(query)
    assert res == [], f"Expected empty result, got {res}"

def check_presence(data, table, expectation):
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
    assert results == expectation

class Query1:
    def test_empty1():
        # tries to select on an empty database
        return assert_empty(QUERIES[0])

    def test_validate1():
        # selects and check if the results match the expectation
        data = Frames.daily
        data['date'] = pd.to_datetime(data['date'])  # Ensure date column is in datetime format
        data['row_sum'] = data.apply(
            lambda row: sum([x for x in row if isinstance(x, int)]), axis=1
            )
        x_values = data['date'].tolist()
        y_values = data['row_sum'].tolist()
        expectation = (x_values, y_values)
        que = Queries(DB, TXT_FILE)
        assert expectation == que.select_query(QUERIES[0])

class Query2:
    def test_insertion2():
        # inserts and checks if is present
        query = Queries[1]
        data = re.search(r'VALUES\s*\((.*?)\)', query)
        que = Queries(DB, TXT_FILE)
        que.mod_query(query)
        return check_presence(data, 'Dates', list(data))

    def duplicate_test2():
        with pytest.raises(sqlite3.IntegrityError):
            que = Queries(DB, TXT_FILE)
            que.mod_query(QUERIES[1])

class Query3:
    def test_presence3(deleted_row):
        que = Queries(DB, TXT_FILE)
        deleted_row = que.del_query(QUERIES[2])
        return check_presence(deleted_row, 'Dates', [])

    def test_delete_not_present3():
        que = Queries(DB, TXT_FILE)
        with pytest.raises(sqlite3.DatabaseError): # is this the correct error
            que.del_query(QUERIES[2])
            
class Query4:
    def test_presence4():
        # modfity the row and check it is has been modified
        expectation = (1419, '2024-01-08')
        que = Queries(DB, TXT_FILE)
        que.mod_query(QUERIES[3])
        return check_presence(expectation, 'Dates', expectation)

    def test_not_exist4():
        # check if the previous val exists
        data = [1418, '2024-01-08']
        return check_presence(data, 'Dates', [])

class Query5:
    def test_validate5():
        cutoff_date = pd.to_datetime("2024-05-05")
        Frames.daily['date'] = pd.to_datetime(Frames.daily['date'])
        df = Frames.daily[Frames.daily['date'] <= cutoff_date]
        schools_closed = df['schools_closed'].tolist().count(1)
        pubs_closed = df['pubs_closed'].tolist().count(1)
        shops_closed = df['shops_closed'].tolist().count(1)
        eating_closed = df['eating_places_closed'].tolist().count(1)
        stay_at_home = df['stay_at_home'].tolist().count(1)
        mixing = df['household_mixing_indoors_banned'].tolist().count(1)
        wfh = df['wfh'].tolist().count(1)
        rule6 = df['rule_of_6_indoors'].tolist().count(1)
        curfew = df['curfew'].tolist().count(1)
        eat_out = df['eat_out_to_help_out'].tolist().count(1)
        expectation = [
            (0, schools_closed), 
            (1, pubs_closed),
            (2, shops_closed),
            (3, eating_closed),
            (4, stay_at_home),
            (5, mixing), 
            (6, wfh), 
            (7, rule6), 
            (8, curfew), 
            (9, eat_out)
            ]
        print(expectation)
        # assert expectation == que.select_query(QUERIES[4])

        

    def test_empty5():
        return assert_empty(QUERIES[4])

class Query6:
    def test_empty6():
        return assert_empty(QUERIES[5])

    def validate6():
        with pytest.raises(sqlite3.DatabaseError):
            que = Queries(DB, TXT_FILE)
            que.select_query(QUERIES[5])

def main():
    daily_path = "coursework1/datasets/restrictions_daily.csv"
    weekly_path = "coursework1/datasets/restrictions_weekly.csv"
    summary_path = "coursework1/datasets/restrictions_summary.csv"
    tables = Tables(
        DB,
        daily_path=daily_path,
        weekly_path=weekly_path,
        summary_path=summary_path
    )

    # Test Query 1
    Query1.test_empty1()
    tables.t_date()
    Query1.test_validate1()

    # Test Query 2
    Query2.test_insertion2()
    Query2.duplicate_test2()

    # Test Query 3
    Query3.test_presence3()
    Query3.test_delete_not_present3()

    # Test Query 4
    Query4.test_presence4()
    Query4.test_not_exist4()

    # Test Query 5
    Query5.test_empty5()

    # Test Query 6
    Query6.test_empty6()

if __name__ == "__main__":
    # Query5.test_validate5()
    print('works')







    
    
    