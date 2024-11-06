import pandas as pd 

class Frames:
    def __init__(self, daily_path: str, weekly_path: str, summary_path: str) -> None:
        self.daily = pd.read_csv(daily_path).dropna()
        self.weekly = pd.read_csv(weekly_path).dropna()
        self.summary =  pd.read_csv(summary_path).dropna()
        self.dates_map = {date: idx for idx, date in enumerate(self.daily['date'].tolist())}
        self.weeks_map = {week_start: idx for idx, week_start in enumerate(self.weekly['week_start'].tolist())}
        self.restrs_map = {restr: i for i, restr in enumerate(self.summary.columns.tolist()[3:])}
        self.sources_map = {s: i for i, s in enumerate(set(self.summary['source']))}

    def get_date_df(self) -> pd.DataFrame:
        return pd.DataFrame(list(self.dates_map.items()), columns=["date_id", "date"])

    def get_week_df(self)-> pd.DataFrame:
        return pd.DataFrame(list(self.weeks_map.items()), columns=["week_id", "week_start"])

    def get_restriction_df(self) -> pd.DataFrame:
        return pd.DataFrame(list(self.restrs_map.items()), columns=['restriction', 'id'])

    def get_source_df(self) -> pd.DataFrame:
        return pd.DataFrame(list(self.sources_map.items()), columns=['source', 'id'])

    def get_summary_restriction_df(self) -> pd.DataFrame:
        dates_lst = self.summary['date'].tolist()
        sources_lst = self.summary['source'].tolist()
        source_ids = [self.sources_map[src] for src in sources_lst]
        res = []
        for i, d in enumerate(dates_lst):
            for restr in self.restrs_map.keys():
                res.append(
                    {
                        'date_id':self.dates_map[d], 
                        'source_id':source_ids[i], 
                        'restriction_id':self.restrs_map[restr], 
                        'in_place': int(self.summary[restr][i])
                    }
                )
        return pd.DataFrame(res)

    def get_daily_restriction_df(self) -> pd.DataFrame:
        dates_lst = self.daily['date'].tolist()
        res = []
        for i, d in enumerate(dates_lst):
            for restr in self.restrs_map.keys():
                res.append(
                    {
                        'date_id':self.dates_map[d], 
                        'restriction_id':self.restrs_map[restr], 
                        'in_place': int(self.daily[restr][i])
                    }
                    )
        return pd.DataFrame(res)

    def get_weekly_restriction_df(self) -> pd.DataFrame:
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