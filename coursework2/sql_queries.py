import sqlite3

class Queries:
    def __init__(self, db, txt_file) -> None:
        self._db = db
        self.queries = self.get_queries(txt_file)

    @staticmethod
    def get_queries(txt_file):
        queries = []
        with open(txt_file, 'r') as file:
            lines = file.readlines()
            current_query = ""
            for line in lines:
                current_query += line
                if line.strip().endswith(';'):
                    queries.append(current_query.strip())
                    current_query = ""
        return queries
    
    def select_query(self, query):
        with sqlite3.connect(self._db) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Query successful")
                return results
            except sqlite3.DatabaseError as db_err:
                print(f"Database error occurred: {db_err}")
                return

    def mod_query(self, query):
        with sqlite3.connect(self._db) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                print("Query successful")
            except sqlite3.DatabaseError as db_err:
                print(f"Database error occurred: {db_err}")
            return

    def del_query(self, query):
        with sqlite3.connect(self._db) as conn:
            cursor = conn.cursor()
            try:
                if "WHERE" in query:
                    table_name = query.split("FROM")[1].split("WHERE")[0].strip()
                    where_clause = query.split("WHERE")[1].strip()
                else:
                    table_name = query.split("FROM")[1].strip()
                    where_clause = ""
                select_query = f"SELECT * FROM {table_name} WHERE {where_clause}" if where_clause else f"SELECT * FROM {table_name}"
                cursor.execute(select_query)
                deleted_rows = cursor.fetchall()
                cursor.execute(query)
                conn.commit()
                print("Query successful")
                return deleted_rows
            except sqlite3.DatabaseError as db_err:
                print(f"Database error occurred: {db_err}")
                return []

def main():
    queries = Queries("..coursework1/database_creation/covid.db", "queries.txt")
    restrictions = queries.select_query(queries.queries_list[0])
    queries.mod_query(queries.queries_list[1])
    queries.mod_query(queries.queries_list[2])
    queries.mod_query(queries.queries_list[3])
    restrictions = queries.select_query(queries.queries_list[4])
    restrictions = queries.select_query(queries.queries_list[5])




