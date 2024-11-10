"""
This script provides the Frames class, which loads and preprocesses COVID-19 restriction
datasets for further database operations. The class converts CSV data into DataFrames
structured for efficient database insertion.

Classes:
    - Frames: Loads daily, weekly, and summary datasets and provides methods to
      retrieve processed DataFrames for dates, weeks, restrictions, sources, and
      various restriction summaries.
"""
import pandas as pd

class Frames:
    """
    Loads and processes COVID-19 restriction data from daily, weekly, and summary CSV files.

    Attributes:
        daily (pd.DataFrame): DataFrame containing daily restriction data.
        weekly (pd.DataFrame): DataFrame containing weekly restriction data.
        summary (pd.DataFrame): DataFrame containing summary restriction data.
        dates_map (dict): Maps dates to unique IDs for the daily dataset.
        weeks_map (dict): Maps week start dates to unique IDs for the weekly dataset.
        restrs_map (dict): Maps restriction types to unique IDs.
        sources_map (dict): Maps source names to unique IDs.
    """
    def __init__(self, daily_path: str, weekly_path: str, summary_path: str) -> None:
        """
        Initializes the Frames class by loading and processing the daily, weekly,
        and summary CSV datasets.

        Parameters:
            daily_path (str): Path to the daily dataset CSV file.
            weekly_path (str): Path to the weekly dataset CSV file.
            summary_path (str): Path to the summary dataset CSV file.
        """
        self.daily = pd.read_csv(daily_path)
        self.weekly = pd.read_csv(weekly_path)
        self.summary =  pd.read_csv(summary_path).dropna()
        self.dates_map = {date: idx for idx, date in enumerate(self.daily['date'].tolist())}
        self.weeks_map = {
            week_start: idx for idx, week_start in enumerate(self.weekly['week_start'].tolist())
            }
        self.restrs_map = {restr: i for i, restr in enumerate(self.summary.columns.tolist()[3:])}
        self.sources_map = {s: i for i, s in enumerate(set(self.summary['source']))}

    def get_date_df(self) -> pd.DataFrame:
        """
        Retrieves a DataFrame mapping each unique date to a date ID.

        Returns:
            pd.DataFrame: DataFrame with columns 'date_id' and 'date'.
        """
        return pd.DataFrame(list(self.dates_map.items()), columns=["date_id", "date"])

    def get_week_df(self)-> pd.DataFrame:
        """
        Retrieves a DataFrame mapping each unique week start date to a week ID.

        Returns:
            pd.DataFrame: DataFrame with columns 'week_id' and 'week_start'.
        """
        return pd.DataFrame(list(self.weeks_map.items()), columns=["week_id", "week_start"])

    def get_restriction_df(self) -> pd.DataFrame:
        """
        Retrieves a DataFrame mapping each restriction type to a unique ID.

        Returns:
            pd.DataFrame: DataFrame with columns 'restriction' and 'id'.
        """
        return pd.DataFrame(list(self.restrs_map.items()), columns=['restriction', 'id'])

    def get_source_df(self) -> pd.DataFrame:
        """
        Retrieves a DataFrame mapping each source name to a unique ID.

        Returns:
            pd.DataFrame: DataFrame with columns 'source' and 'id'.
        """
        return pd.DataFrame(list(self.sources_map.items()), columns=['source', 'id'])

    def get_summary_restriction_df(self) -> pd.DataFrame:
        """
        Retrieves a DataFrame summarizing restrictions with date, source, and restriction IDs.

        Returns:
            pd.DataFrame: DataFrame with columns:
                'date_id',
                'source_id',
                'restriction_id',
                'in_place'.
        """
        dates_lst = self.summary['date'].tolist()
        sources_lst = self.summary['source'].tolist()
        source_ids = [self.sources_map[src] for src in sources_lst]
        res = []
        for i, date in enumerate(dates_lst):
            for restr in self.restrs_map.keys():
                res.append(
                    {
                        'date_id':self.dates_map[date],
                        'source_id':source_ids[i],
                        'restriction_id':self.restrs_map[restr],
                        'in_place': int(self.summary[restr][i])
                    }
                )
        return pd.DataFrame(res)

    def get_daily_restriction_df(self) -> pd.DataFrame:
        """
        Retrieves a DataFrame of daily restrictions with date and restriction IDs.

        Returns:
            pd.DataFrame: DataFrame with columns 'date_id', 'restriction_id', and 'in_place'.
        """
        dates_lst = self.daily['date'].tolist()
        res = []
        for i, date in enumerate(dates_lst):
            for restr in self.restrs_map.keys():
                res.append(
                    {
                        'date_id':self.dates_map[date],
                        'restriction_id':self.restrs_map[restr],
                        'in_place': int(self.daily[restr][i])
                    }
                    )
        return pd.DataFrame(res)

    def get_weekly_restriction_df(self) -> pd.DataFrame:
        """
        Retrieves a DataFrame of weekly restrictions with week start date and restriction IDs.

        Returns:
            pd.DataFrame: DataFrame with columns 'week_id', 'restriction_id', and 'in_place'.
        """
        weeks_lst = self.weekly['week_start'].tolist()
        res = []
        for i, week in enumerate(weeks_lst):
            for restr in self.restrs_map.keys():
                res.append(
                    {
                        'week_id':self.weeks_map[week],
                        'restriction_id':self.restrs_map[restr],
                        'in_place': int(self.weekly[restr][i])
                    }
                )
        return pd.DataFrame(res)
