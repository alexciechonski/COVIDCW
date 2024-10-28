This project is part of the COMP0035 module coursework and demonstrates the process of data exploration, preparation, and database design.
The project includes Python scripts to explore and clean the dataset, as well as to create and populate an SQLite database.

Project Structure

Dataset
The dataset used in this project is sourced from https://data.london.gov.uk/dataset/covid-19-restrictions-timeseries. It is licensed under UK Open Government Licence, which can be found here https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.


Setup and Installation
1. Clone the repository:
    git clone https://github.com/alexciechonski/COVIDCW

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
