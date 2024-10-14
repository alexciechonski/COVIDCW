import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    daily = pd.read_csv("restrictions_daily.csv")
    weekly = pd.read_csv("restrictions_weekly.csv")
    summary = pd.read_csv("restrictions_summary.csv")
    return daily, weekly, summary

def get_col_names(df: pd.DataFrame, name: str) -> str:
    cols_str = ", ".join(list(df.columns))
    return f"Columns of the {name} dataframe are: {cols_str}"

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

def cumulative_data(df):
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
    
def plot_cumulative(data_dict: dict, title: str):
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
    plt.show()

def timeline(df):
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
    plt.title('Total number of restrictions enforced per da')
    
    # Rotate x-tick labels if names are too long
    plt.xticks(rotation=45, ha='right')
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    daily, weekly, summary = get_data()
    print(summary['restriction'])

    # timeline(daily)

    # cumulative = cumulative_data(daily)
    # plot_cumulative(cumulative, 'days')
    
    # # dataframe shapes
    # print(f"daily shape: {daily.shape}")
    # print(f"weekly shape: {weekly.shape}")
    # print(f"summary shape: {summary.shape}")

    # # dataframe data types
    # print("daily datatypes:")
    # print(get_types(daily))
    # print("weekly datatypes")
    # print(get_types(weekly))
    # print('summary datatypes')
    # print(get_types(summary))
    
    # # column names
    # print(get_col_names(daily, 'daily'))
    # print(get_col_names(weekly, 'weekly'))
    # print(get_col_names(summary, 'summary'))

if __name__ == "__main__":
    main()