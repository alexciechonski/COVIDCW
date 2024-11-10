"""
main.py

This script loads, explores, and prepares COVID-19 restriction datasets for analysis.
It uses the following classes:
- DataLoader: Loads daily, weekly, and summary data from CSV files.
- DataExploration: Provides functions for logging data shapes, types, and column names.
- DataPreparation: Generates visualizations, including a cumulative restriction timeline,
  a bar chart for days restrictions were enforced, and a restriction timeline plot.

Functions:
- main(): Executes the data loading, exploration, and preparation workflow.

Usage:
Run this script as a standalone program to generate exploration logs and visualizations.
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from coursework1.data_exploration.utils import save_to_csv # pylint: disable = import-error

class DataLoader:
    """
    Loads data from csv to pd.DataFrame

    Attributes:
        path_daily (str): Path to the daily data csv file.
        path_weekly (str): Path to the weekly data csv file.
        path_summary (str): Path to the summary data csv file.
    """
    def __init__(self, path_daily: str, path_weekly: str, path_summary: str) -> None:
        """
        Initializes DataLoader with paths to daily, weekly, and summary CSV files.

        Parameters:
        path_daily (str): Path to the daily data CSV file.
        path_weekly (str): Path to the weekly data CSV file.
        path_summary (str): Path to the summary data CSV file.
        """
        self.path_daily = path_daily
        self.path_weekly = path_weekly
        self.path_summary = path_summary

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Loads the daily, weekly, and summary datasets from CSV files.

        Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        DataFrames for daily, weekly, and summary datasets.
        """
        daily = pd.read_csv(self.path_daily)
        weekly = pd.read_csv(self.path_weekly)
        summary = pd.read_csv(self.path_summary)
        return daily, weekly, summary

class DataExploration:
    """
    Class of functions for data exploration

    Attributes:
        daily (pd.DataFrame): Daily DataFrame.
        weekly (pd.DataFrame): Weekly DataFrame.
        summary (pd.DataFrame): Summary DataFrame.
    """
    def __init__(self, daily: pd.DataFrame, weekly: pd.DataFrame, summary: pd.DataFrame) -> None:
        """
        Initializes DataExploration with daily, weekly, and summary data.

        Parameters:
        daily (pd.DataFrame): DataFrame containing daily data.
        weekly (pd.DataFrame): DataFrame containing weekly data.
        summary (pd.DataFrame): DataFrame containing summary data.
        """
        self.daily = daily
        self.weekly = weekly
        self.summary = summary.dropna()

    @staticmethod
    def get_col_names(data: pd.DataFrame) -> list[str]:
        """
        Retrieves the column names from a DataFrame.

        Parameters:
        data (pd.DataFrame): DataFrame from which to extract column names.

        Returns:
        list[str]: List of column names in the DataFrame.
        """
        return list(data.columns)

    @staticmethod
    def get_types(data: pd.DataFrame) -> dict[str, str]:
        """
        Retrieves data types of each column in a DataFrame.

        Parameters:
        data (pd.DataFrame): DataFrame from which to extract data types.

        Returns:
        dict[str, str]: Dictionary with column names as keys and data types as values.
        """
        return {col: str(data[col].dtype) for col in data.columns}

    @staticmethod
    def get_data_range(data: pd.DataFrame) -> dict[str:str]:
        """
        Computes the range of values for integer columns in a DataFrame.

        Parameters:
        data (pd.DataFrame): DataFrame for which to calculate column ranges.

        Returns:
        dict[str:str]: Dictionary with column names as keys and ranges as values
        for integer columns.
        """
        result = {}
        for col in data.columns:
            if pd.api.types.is_integer_dtype(data[col]):
                result[col] = f"{min(data[col])}-{max(data[col])}"
            else:
                result[col] = None
        return result

    def get_data_shapes(self, output_file: str) -> None:
        """
        Writes the shapes of daily, weekly, and summary data to an output file.

        Parameters:
        output_file (str): File path where data shapes will be saved.
        """
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write("DATA SHAPES\n")
            file.write(f"daily data shape: {self.daily.shape}\n")
            file.write(f"weekly data shape: {self.weekly.shape}\n")
            file.write(f"summary data shape: {self.summary.shape}\n")
            file.write("\n")

    def get_data_types(self, output_file: str) -> None:
        """
        Writes the data types of daily, weekly, and summary data to an output file.

        Parameters:
        output_file (str): File path where data types will be saved.
        """
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write("DATA TYPES\n")
            file.write(
                f"daily data types: {json.dumps(self.get_types(self.daily), indent=2)}\n"
                )
            file.write(
                f"weekly data types: {json.dumps(self.get_types(self.weekly), indent=2)}\n"
                )
            file.write(
                f"summary data types: {json.dumps(self.get_types(self.summary), indent=2)}\n"
                )
            file.write("\n")

    def get_columns(self, output_file: str) -> None:
        """
        Writes the column names of daily, weekly, and summary data to an output file.

        Parameters:
        output_file (str): File path where column names will be saved.
        """
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write("COLUMNS\n")
            file.write(
                f"daily columns: {json.dumps(self.get_col_names(self.daily), indent=2)}\n"
                )
            file.write(
                f"weekly columns: {json.dumps(self.get_col_names(self.weekly), indent=2)}\n"
                )
            file.write(
                f"summary columns: {json.dumps(self.get_col_names(self.summary), indent=2)}\n"
                )
            file.write("\n")

class DataPreparation:
    """
    Class of functions for data preparation

    Attributes:
        daily (pd.DataFrame): Daily DataFrame.
        weekly (pd.DataFrame): Weekly DataFrame.
        summary (pd.DataFrame): Summary DataFrame.
    """
    def __init__(self, daily: pd.DataFrame, weekly: pd.DataFrame, summary: pd.DataFrame) -> None:
        """
        Initializes DataPreparation with daily, weekly, and summary data.

        Parameters:
        daily (pd.DataFrame): DataFrame containing daily data.
        weekly (pd.DataFrame): DataFrame containing weekly data.
        summary (pd.DataFrame): DataFrame containing summary data.
        """
        self.daily = daily
        self.weekly = weekly
        self.summary = summary.dropna()

    def num_days_closed(self) -> dict[str,int]:
        """
        Calculates the number of days different types of restrictions were enforced and
        saves the data.

        Parameters:
        data (pd.DataFrame): DataFrame with restriction data.

        Returns:
        dict[str, int]: Dictionary with restriction types as keys and count of
        days enforced as values.
        """
        schools_closed = self.daily['schools_closed'].tolist().count(1)
        pubs_closed = self.daily['pubs_closed'].tolist().count(1)
        shops_closed = self.daily['shops_closed'].tolist().count(1)
        eating_closed = self.daily['eating_places_closed'].tolist().count(1)
        mixing = self.daily['household_mixing_indoors_banned'].tolist().count(1)
        wfh = self.daily['wfh'].tolist().count(1)
        rule6 = self.daily['rule_of_6_indoors'].tolist().count(1)
        curfew = self.daily['curfew'].tolist().count(1)
        eat_out = self.daily['eat_out_to_help_out'].tolist().count(1)
        res = {
            'schools': schools_closed,
            'pubs_closed': pubs_closed,
            'shops_closed': shops_closed,
            'eating_closed': eating_closed,
            'mixing': mixing,
            'wfh': wfh,
            'rule6': rule6,
            'curfew': curfew,
            'eat_out': eat_out
        }
        return res

    @staticmethod
    def plot_num_days_closed(data_dict: dict, folder_path: str) -> None:
        """
        Creates and saves a bar chart showing the number of days each restriction was enforced.

        Parameters:
        data_dict (dict): Dictionary with restriction types and counts of days enforced.
        folder_path (str): Path where the plot image will be saved.
        """
        names = list(data_dict.keys())
        values = list(data_dict.values())

        plt.figure(figsize=(10, 6))
        plt.bar(names, values, color='skyblue')

        plt.xlabel('Restriction Type')
        plt.ylabel('Total number of days enforced:')
        plt.title('Bar Chart')

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.savefig(f'{folder_path}/num_days_closed.png')

    @staticmethod
    def cumulative_timeline_data(data: pd.DataFrame) -> dict:
        """
        Creates a line plot showing the cumulative number of restrictions enforced in time.

        Parameters:
        data (pd.DataFrame): DataFrame with restriction data including date and restriction columns.
        folder_path (str): Path where the plot image will be saved.
        """
        data['date'] = pd.to_datetime(data['date'])  # Ensure date column is in datetime format
        data['row_sum'] = data.apply(
            lambda row: sum([x for x in row if isinstance(x, int)]), axis=1
            )
        x_values = data['date'].tolist()
        y_values = data['row_sum'].tolist()
        return {
            "x_vals": x_values,
            "y_vals": y_values
        }

    @staticmethod
    def plot_cumulative_timeline(xy_dict: dict, folder_path: str) -> None:
        """
        Generates and saves a cumulative timeline plot of restrictions enforced over time.

        This static method creates a line plot based on the x and y values
        provided in the dictionary.
        The plot displays the cumulative number of restrictions enforced each day,
        with labels and a title for clarity. The resulting plot is saved as a PNG file.

        Parameters:
        - xy_dict (dict): A dictionary containing data for the plot. Expected keys are:
                        - 'x_vals': List of values for the x-axis.
                        - 'y_vals': List of values for the y-axis.
        - folder_path (str): The folder path where the plot image will be saved.
        """
        x_values = xy_dict['x_vals']
        y_values = xy_dict['y_vals']
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, color='skyblue')

        plt.xlabel('Restriction Type')
        plt.ylabel('Total number of restrictions enforced:')
        plt.title('Total number of restrictions enforced per day')

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.savefig(f'{folder_path}/cumulative_timeline.png')

    def restriction_timeline_data(self) -> pd.DataFrame:
        """
        Creates and saves a timeline plot showing the sequence of restrictions over time.

        Parameters:
        folder_path (str): Path where the plot image will be saved.
        """
        levels = [-5, -3, -1, 1, 3, 5]
        self.summary['level'] = [levels[i % len(levels)] for i in range(len(self.summary))]
        data = self.summary[['date','restriction','level']]
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        return data

    @staticmethod
    def plot_restriction_timeline(data: pd.DataFrame, folder_path: str) -> None:
        """
        Plots a cumulative timeline graph of restrictions enforced over time
        and saves it as a PNG file.

        Parameters:
        - xy_dict (dict): A dictionary containing x and y values for the plot.
            Expected keys are 'x_vals' for the x-axis data (dates)
            and 'y_vals' for the y-axis data (restriction counts).
        - folder_path (str): The folder path where the plot image will be saved.
        """
        _,  axis = plt.subplots(figsize=(18,9))
        axis.plot(data['date'], [0,]*len(data), "-o", color="black", markerfacecolor="white")
        axis.set_ylim(-7,7)

        for i in range(len(data)):
            date, event, level = data['date'][i], data['restriction'][i], data['level'][i]
            y_offset = level + 0.5 * (-1)**i  # Stagger labels slightly
            axis.annotate(
                event,
                xy=(date, 0.1 if level>0 else -0.1),
                xytext=(date, y_offset),
                textcoords='data',
                ha = "center",
                va = 'bottom' if level > 0 else 'top',
                fontsize=5,
                rotation=25,
                arrowprops=dict(arrowstyle="-", color="red", linewidth=0.5)
                )

        axis.spines[['left', 'top', 'bottom', 'right']].set_visible(False)
        axis.yaxis.set_visible(False)
        plt.savefig(f'{folder_path}/restriction_timeline.png')

def main() -> None:
    """Loads, explores and prepares the data"""
    # Dataset Attribution:
    # Contains public sector information licensed under the Open Government Licence v3.0.
    # Source:
    # COVID-19 Restrictions Timeseries dataset, Greater London Authority (GLA), London Datastore
    data_loader = DataLoader(
        "coursework1/datasets/restrictions_daily.csv",
        "coursewrk1/datasets/restrictions_weekly.csv",
        "coursework1/datasets/restrictions_summary.csv"
        )
    daily, weekly, summary = data_loader.load_data()

    # Data Exploration Summaries
    output_file = "coursework1/data_exploration/prepared_data/data.txt"
    explo = DataExploration(daily, weekly, summary)
    explo.get_data_shapes(output_file) # dataframe shapes
    explo.get_data_types(output_file) # dataframe data types
    explo.get_columns(output_file) # column names

    # Data Preparation
    folder_path = "coursework1/data_exploration/prepared_data/figs"
    data_path = "coursework1/data_exploration/prepared_data"
    prep = DataPreparation(daily, weekly, summary)

    # plot timeline graph
    timeline_data = prep.cumulative_timeline_data(daily)
    save_to_csv(timeline_data, 'timeline_data.csv', data_path)

    # plot number of days closed bar chart
    num_days_closed = prep.num_days_closed()
    save_to_csv(num_days_closed, 'num_days_closed.csv', data_path)
    prep.plot_num_days_closed(num_days_closed, folder_path)

    # plot restriction timelime
    restriction_data = prep.restriction_timeline_data()
    save_to_csv(restriction_data, 'restriction_data.csv', data_path)
    prep.plot_restriction_timeline(restriction_data, folder_path)

if __name__ == "__main__":
    main()
