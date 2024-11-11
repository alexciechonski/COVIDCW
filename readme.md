This project is part of the COMP0035 module coursework and demonstrates the process of data exploration, preparation, and database design.
The project includes Python scripts to explore and clean the dataset, as well as to create and populate an SQLite database.

Project Structure
COVIDCW
comp0035-cw-alexciechonski/
│
├── coursework1/
│   ├── data_exploration/
│   │   ├── prepared_data/
│   │   │   ├── figs/
│   │   │   │   ├── cumulative_times.png
│   │   │   │   ├── num_days_closed.png
│   │   │   │   └── restriction_times.png
│   │   │   ├── data.txt
│   │   │   ├── num_days_closed.csv
│   │   │   ├── restriction_data.csv
│   │   │   └── timeline_data.csv
│   │   ├── main.py
│   │   └── utils.py
│   │
│   ├── database_creation/
│   │   ├── covid.db
│   │   ├── create_db.py
│   │   ├── frames.py
│   │   └── relations.vuerd.json
│   │
│   ├── datasets/
│   │   ├── restrictions_daily.csv
│   │   ├── restrictions_summary.csv
│   │   └── restrictions_weekly.csv
│   │
│   └── __init__.py
│
├── coursework2/
│   └── __init__.py
│
├── venv/
│
├── .gitignore
├── pyproject.toml
├── readme.md
└── requirements.txt

Dataset
The dataset used in this project is sourced from https://data.london.gov.uk/dataset/covid-19-restrictions-timeseries. It is licensed under the UK Open Government Licence, which can be found here https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.


Setup and Installation
1. Clone the repository:
    git clone https://github.com/ucl-comp0035/comp0035-cw-alexciechonski
    cd comp0035-cw-alexciechonski

2. Create and activate a virtual environment:
    Mac OS/Linux:
    python3 -m venv venv
    source venv/bin/activate

    Windows:
    python3 -m venv venv
    venv\Scripts\activate

3. Install the requirements
    pip install -r requirements.txt
    
4. Install the project in editable mode
    pip install -e .

Linting
PyLint has been used for linting
