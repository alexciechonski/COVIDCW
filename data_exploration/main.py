import pandas as pd
import matplotlib.pyplot as plt
import json

def get_data(path_daily, path_weekly, path_summary):
    # Dataset source: COVID-19 Restrictions Timeseries, owned by GLAGIS, licensed under UK Open Governemnt Licence
    daily = pd.read_csv(path_daily)
    weekly = pd.read_csv(path_weekly)
    summary = pd.read_csv(path_summary)
    return daily, weekly, summary

def get_col_names(df: pd.DataFrame) -> str:
    return list(df.columns)
    # return f"Columns of the {name} dataframe are: {cols_str}"

def get_types(df):
    return {col: str(df[col].dtype) for col in df.columns}

def get_data_range(df):
    result = {}
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            result[col] = f"{min(df[col])}-{max(df[col])}"
        else:
            result[col] = None
    return result

def get_closed_stats(df, time_unit):
    schools_closed = df['schools_closed'].tolist()
    pubs_closed = df['pubs_closed'].tolist()
    shops_closed = df['shops_closed'].tolist()
    eating_closed = df['eating_places_closed'].tolist()
    time = df[time_unit]
    all_closed = sum(1 for a, b, c, d in zip(schools_closed, pubs_closed, shops_closed, eating_closed) if a == b == c == d == 1)
    return time, schools_closed.count(1), pubs_closed.count(1), shops_closed.count(1), eating_closed.count(1), all_closed

def num_days_closed(df):
    schools_closed = df['schools_closed'].tolist().count(1)
    pubs_closed = df['pubs_closed'].tolist().count(1)
    shops_closed = df['shops_closed'].tolist().count(1)
    eating_closed = df['eating_places_closed'].tolist().count(1)
    mixing = df['household_mixing_indoors_banned'].tolist().count(1)
    wfh = df['wfh'].tolist().count(1)
    rule6 = df['rule_of_6_indoors'].tolist().count(1)
    curfew = df['curfew'].tolist().count(1)
    eat_out = df['eat_out_to_help_out'].tolist().count(1)
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
    
def plot_num_days_closed(data_dict: dict, title: str):
    # Ensure that both keys and values are in the correct format
    names = list(data_dict.keys())  # Assuming keys are hashable (e.g., strings)
    values = list(data_dict.values())  # Convert Series to list if needed
    
    # Create a figure and plot a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(names, values, color='skyblue')
    
    # Add labels and title
    plt.xlabel('Restriction Type')
    plt.ylabel(f'Total number of {title} enforced:')
    plt.title('Bar Chart')
    
    # Rotate x-tick labels if names are too long
    plt.xticks(rotation=45, ha='right')
    
    # Show the plot
    plt.tight_layout()
    # plt.show()
    plt.savefig('data_exploration/prepared_data/num_days_closed.png')


def cumulative_timeline(df):
    df['date'] = pd.to_datetime(df['date'])  # Ensure date column is in datetime format
    df['row_sum'] = df.apply(lambda row: sum([x for x in row if isinstance(x, int)]), axis=1)
    x = df['date'].tolist()
    y = df['row_sum'].tolist()

    # Create a figure and plot a bar chart
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, color='skyblue')
    
    # Add labels and title
    plt.xlabel('Restriction Type')
    plt.ylabel('Total number of restrictions enforced:')
    plt.title('Total number of restrictions enforced per day')
    
    # Rotate x-tick labels if names are too long
    plt.xticks(rotation=45, ha='right')
    
    # Show the plot
    plt.tight_layout()
    # plt.show()
    plt.savefig('data_exploration/prepared_data/cumulative_timeline.png')

def plot_restriction_timeline(summary):
    summary = summary.dropna()
    levels = [-5, -3, -1, 1, 3, 5]
    summary['level'] = [levels[i % len(levels)] for i in range(len(summary))]
    df = summary[['date','restriction','level']]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # print(df)

    # timeline
    fig, ax = plt.subplots(figsize=(18,9))
    ax.plot(df['date'], [0,]*len(df), "-o", color="black", markerfacecolor="white")
    ax.set_ylim(-7,7)

    for i in range(len(df)):
        date, event, level = df['date'][i], df['restriction'][i], df['level'][i]
        y_offset = level + 0.5 * (-1)**i  # Stagger labels slightly
        ax.annotate(
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

    ax.spines[['left', 'top', 'bottom', 'right']].set_visible(False)
    ax.yaxis.set_visible(False)
    # plt.show()
    plt.savefig('data_exploration/prepared_data/restriction_timeline.png')

def get_data_shapes(daily, weekly, summary, output_file):
    with open(output_file, 'a') as f:
            f.write("DATA SHAPES\n")
            f.write(f"daily data shape: {daily.shape}\n")
            f.write(f"weekly data shape: {weekly.shape}\n")
            f.write(f"summary data shape: {summary.shape}\n")
            f.write("\n")

def get_data_types(daily, weekly, summary, output_file):
    with open(output_file, 'a') as f:
        f.write("DATA TYPES\n")
        f.write(f"daily data types: {get_types(daily)}\n")
        f.write(f"weekly data types: {get_types(weekly)}\n")
        f.write(f"summary data types: {get_types(summary)}\n")
        f.write("\n")

def get_columns(daily, weekly, summary, output_file):
    with open(output_file, 'a') as f:
        f.write("COLUMNS\n")
        f.write(f"daily columns: {json.dumps(get_col_names(daily), indent=2)}\n")
        f.write(f"weekly columns: {json.dumps(get_types(weekly), indent=2)}\n")
        f.write(f"summary columns: {json.dumps(get_types(summary), indent=2)}\n")
        f.write("\n")

def main():
    daily, weekly, summary = get_data(
        "datasets/restrictions_daily.csv", 
        "datasets/restrictions_weekly.csv", 
        "datasets/restrictions_summary.csv"
        )

    # # dataframe shapes
    # get_data_shapes(daily, weekly, summary, "data_exploration/prepared_data/data.txt")

    # # dataframe data types
    # get_data_types(daily, weekly, summary, "data_exploration/prepared_data/data.txt")
    
    # # column names
    # get_columns(daily, weekly, summary, "data_exploration/prepared_data/data.txt")

    # cumulative_timeline(daily)

    # plot_num_days_closed(num_days_closed(daily), 'days')

    plot_restriction_timeline(summary)

if __name__ == "__main__":
    main()