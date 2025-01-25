from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine, text
from typing import List
import logging
from pathlib import Path
from src.settings import console

DATA_DIR = Path('./data')

def scrape_table(data: str, date: str) -> None:
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', {'id': 'headFixed'})

    # Check if the table contains "No Record Found"
    no_record_found = table.find('td', text='No Record Found.')
    if no_record_found:
        console.log(f"[yellow]Skipping {date}: Market closed or no data available.[/yellow]")
        return  # Skip this day

    if not table:
        logging.warning(f"No table found for {date}")
        return

    headers = get_table_headers(table)
    rows = get_table_rows(table)

    if len(rows) < 2:  # Ensure there are at least two rows (header + data)
        logging.info(f"No record for {date}")
        return

    save_as_csv(headers, rows, date)
    save_to_db(headers, rows, date)

def get_table_headers(table) -> List[str]:
    return [th.text.strip() for th in table.find("tr").find_all("th")]

def get_table_rows(table) -> List[List[str]]:
    rows = []
    for tr in table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        cells = [td.text.strip() for td in tds]

        # Handle the 'Conf' column (replace '-' with NULL or a default value)
        if len(cells) > 1 and cells[1] == '-':  # Assuming 'Conf' is the second column (index 1)
            cells[1] = None  # Replace '-' with NULL for SQLite

        rows.append(cells)
    return rows

def save_to_db(headers: List[str], rows: List[List[str]], date: str):
    engine = create_engine(f'sqlite:///{DATA_DIR}/scraped_data.db')

    with engine.connect() as conn:
        # Create the table if it doesn't exist
        if not conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='share_prices'")).fetchone():
            # Define all possible columns (22 columns)
            columns = [
                "SNo TEXT", "Symbol TEXT", "Conf TEXT", "Open TEXT", "High TEXT", "Low TEXT", "Close TEXT",
                "VWAP TEXT", "Vol TEXT", "PrevClose TEXT", "Turnover TEXT", "Trans TEXT", "Diff TEXT",
                "Range TEXT", "DiffPct TEXT", "RangePct TEXT", "VWAPPct TEXT", "Days120 TEXT", "Days180 TEXT",
                "Weeks52High TEXT", "Weeks52Low TEXT", "date TEXT"
            ]
            conn.execute(text(f"CREATE TABLE share_prices ({', '.join(columns)})"))

        # Insert rows into the table
        for row in rows:
            # Pad the row with NULL values if it has fewer than 21 columns
            if len(row) < 21:
                row += [None] * (21 - len(row))  # Pad with NULL for missing columns

            # Replace empty strings with NULL
            row = [None if cell == '' else cell for cell in row]

            # Add the date column
            row.append(date)

            # Prepare the SQL query
            values = ", ".join([f"'{value}'" if value is not None else "NULL" for value in row])
            conn.execute(text(f"INSERT INTO share_prices VALUES ({values})"))

        conn.commit()


def save_as_csv(headers: List[str], rows: List[List[str]], date: str):
    # Extract the year from the date
    year = date.split('-')[0]  # Assuming date is in 'YYYY-MM-DD' format

    # Create the year-specific directory if it doesn't exist
    year_dir = DATA_DIR / year
    year_dir.mkdir(parents=True, exist_ok=True)

    # Create the CSV file path
    csv_path = year_dir / f"{date}.csv"

    # Save the data as a CSV file
    df = pd.DataFrame(rows, columns=headers)
    df.to_csv(csv_path, index=False)
    console.log(f"Saved {csv_path}")