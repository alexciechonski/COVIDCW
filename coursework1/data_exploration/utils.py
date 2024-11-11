"""
This module provides a utility function to save various data types to a CSV file.

The `save_to_csv` function allows users to save a `pandas.DataFrame` or a dictionary to a CSV file.
It automatically converts the dictionary to a DataFrame before saving and supports specifying the
file name and file path for the output CSV.
"""
from typing import Any
import pandas as pd
def save_to_csv(data: Any, file_name: str, path: str):
    """
    Saves data to a CSV file, supporting both DataFrames and dictionaries.

    This function takes a `pandas.DataFrame` or a dictionary as input and saves it as a CSV file.
    If a dictionary is provided, it is first converted to a single-row DataFrame before saving.
    The resulting CSV file is saved to the specified path with the given file name.

    Parameters:
    - data (Any): The data to save, which can be either a `pandas.DataFrame` or a dictionary.
    - file_name (str): The name of the CSV file (without path).
    - path (str): The directory path where the CSV file will be saved.

    Returns:
    - None
    """
    path = f"{path}/{file_name}"
    if isinstance(data, pd.DataFrame):
        data.to_csv(path, index=False)
    elif isinstance(data, dict):
        converted_data = pd.DataFrame([data])
        converted_data.to_csv(path, index=False)
