import json
import pandas as pd
import matplotlib.pyplot as plt
class DataLoader:
    """Class responsible for loading data from CSV files."""
    def __init__(self, path_daily: str, path_weekly: str, path_summary: str) -> None:
        self.path_daily = path_daily
        self.path_weekly = path_weekly
        self.path_summary = path_summary

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads the daily, weekly, and summary datasets and returns them."""
        daily = pd.read_csv(self.path_daily)
        weekly = pd.read_csv(self.path_weekly)
        summary = pd.read_csv(self.path_summary)
        return daily, weekly, summary

class DataExploration:
    def __init__(self, daily: pd.DataFrame, weekly: pd.DataFrame, summary: pd.DataFrame) -> None:
        self.daily = daily
        self.weekly = weekly
        self.summary = summary.dropna()

    @staticmethod
    def get_col_names(data: pd.DataFrame) -> list[str]:
        return list(data.columns)

    @staticmethod
    def get_types(data: pd.DataFrame) -> dict[str, str]:
        return {col: str(data[col].dtype) for col in data.columns}

    @staticmethod
    def get_data_range(data: pd.DataFrame) -> dict[str:str]:
        result = {}
        for col in data.columns:
            if pd.api.types.is_integer_dtype(data[col]):
                result[col] = f"{min(data[col])}-{max(data[col])}"
            else:
                result[col] = None
        return result

    def get_data_shapes(self, output_file: str) -> None:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write("DATA SHAPES\n")
            file.write(f"daily data shape: {self.daily.shape}\n")
            file.write(f"weekly data shape: {self.weekly.shape}\n")
            file.write(f"summary data shape: {self.summary.shape}\n")
            file.write("\n")

    def get_data_types(self, output_file: str) -> None:
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
    def __init__(self, daily: pd.DataFrame, weekly: pd.DataFrame, summary: pd.DataFrame) -> None:
        self.daily = daily
        self.weekly = weekly
        self.summary = summary.dropna()

    @staticmethod
    def num_days_closed(data: pd.DataFrame) -> dict[str,int]:
        schools_closed = data['schools_closed'].tolist().count(1)
        pubs_closed = data['pubs_closed'].tolist().count(1)
        shops_closed = data['shops_closed'].tolist().count(1)
        eating_closed = data['eating_places_closed'].tolist().count(1)
        mixing = data['household_mixing_indoors_banned'].tolist().count(1)
        wfh = data['wfh'].tolist().count(1)
        rule6 = data['rule_of_6_indoors'].tolist().count(1)
        curfew = data['curfew'].tolist().count(1)
        eat_out = data['eat_out_to_help_out'].tolist().count(1)
        return {
            # 'time': days if days is not None else weeks if weeks is not None else None,
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

    @staticmethod
    def plot_num_days_closed(data_dict: dict, title: str, folder_path: str) -> None:
        names = list(data_dict.keys())
        values = list(data_dict.values())

        plt.figure(figsize=(10, 6))
        plt.bar(names, values, color='skyblue')

        plt.xlabel('Restriction Type')
        plt.ylabel(f'Total number of {title} enforced:')
        plt.title('Bar Chart')

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.savefig(f'{folder_path}/num_days_closed.png')

    @staticmethod
    def cumulative_timeline(data: pd.DataFrame, folder_path: str) -> None:
        data['date'] = pd.to_datetime(data['date'])  # Ensure date column is in datetime format
        data['row_sum'] = data.apply(
            lambda row: sum([x for x in row if isinstance(x, int)]), axis=1
            )
        x_values = data['date'].tolist()
        y_values = data['row_sum'].tolist()

        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, color='skyblue')

        plt.xlabel('Restriction Type')
        plt.ylabel('Total number of restrictions enforced:')
        plt.title('Total number of restrictions enforced per day')

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.savefig(f'{folder_path}/cumulative_timeline.png')

    def plot_restriction_timeline(self, folder_path: str) -> None:
        levels = [-5, -3, -1, 1, 3, 5]
        self.summary['level'] = [levels[i % len(levels)] for i in range(len(self.summary))]
        data = self.summary[['date','restriction','level']]
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

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
    data_loader = DataLoader(
        "datasets/restrictions_daily.csv",
        "datasets/restrictions_weekly.csv",
        "datasets/restrictions_summary.csv"
        )
    daily, weekly, summary = data_loader.load_data()

    # Data Exploration Summaries
    output_file = "data_exploration/prepared_data/data.txt"
    explo = DataExploration(daily, weekly, summary)
    explo.get_data_shapes(output_file) # dataframe shapes
    explo.get_data_types(output_file) # dataframe data types
    explo.get_columns(output_file) # column names

    # Data Preparation
    folder_path = "data_exploration/prepared_data/figs"
    prep = DataPreparation(daily, weekly, summary)

    #plot timeline graph
    prep.cumulative_timeline(daily, folder_path)
    # plot number of days closed bar chart
    prep.plot_num_days_closed(prep.num_days_closed(daily), 'days', folder_path)
    # plot restriction timelime
    prep.plot_restriction_timeline(folder_path)

if __name__ == "__main__":
    main()
