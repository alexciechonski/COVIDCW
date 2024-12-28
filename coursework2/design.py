from ..coursework1.data_exploration.main import DataPreparation
import pandas as pd

class Graph:
    def __init__(self) -> None:
        self.adjency_list = []
    
    def add_node(self, val, edges):
        pass

    def add_edge(self, node_from, node_to):
        pass

    def remove_node(self, node):
        pass

    def remove_edge(self, node_from, node_to):
        pass

    def has_edge(self, node):
        pass

    def has_node(self, node_from, node_to):
        pass

class Database:
    def __init__(self, conn_str) -> None:
        self.conn_str = conn_str
        self.daily = pd.DataFrame()
        self.weekly = pd.DataFrame()
        self.summary = pd.DataFrame()
        self.changes = pd.DataFrame()

    def get_db(self):
        pass

    def get_table(self):
        pass

class CRUD(Database):
    def __init__(self, conn_str) -> None:
        super().__init__(conn_str)

    def create():
        pass

    def read():
        pass

    def update():
        pass

    def delete():
        pass

class ChangesLog(Database):
    def __init__(self, conn_str, new_entry) -> None:
        super().__init__(conn_str)
        self.new_entry = new_entry

    def is_valid(table, constraints):
        pass

class Diagrams(DataPreparation):
    def __init__(self, daily: pd.DataFrame, weekly: pd.DataFrame, summary: pd.DataFrame) -> None:
        super().__init__(daily, weekly, summary)
    
    def plot_lockdown_timeline(self):
        pass

    def plot_bar_graph(self):
        pass

    def restriction_timeline(self):
        pass

    def _goto_page(self, hyperlink):
        pass








