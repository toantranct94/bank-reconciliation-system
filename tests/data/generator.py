import argparse
import csv
import os
import random
from datetime import datetime, timedelta
from uuid import uuid4

from tqdm import tqdm

START_DATE_STR = "01/01/2023 00:00:00"
NUMBER_OF_RECORDS = 1000000
MAX_FILE_SIZE_MB = 9


# Function to generate continuous date strings with a time interval of 1 second
def generate_continuous_dates(start_date_str, num_records):
    date_format = "%d/%m/%Y %H:%M:%S"
    start_date = datetime.strptime(start_date_str, date_format)

    for i in tqdm(range(num_records)):
        current_date = start_date + timedelta(seconds=i)
        date_str = current_date.strftime(date_format)
        yield date_str


# Function to generate random dummy data
def generate_dummy_data(number_of_records=NUMBER_OF_RECORDS):
    dates = generate_continuous_dates(START_DATE_STR, number_of_records)
    for date_str in dates:
        content = "Any text there"
        amount = round(random.uniform(-1000, 1000), 3)
        types = ["Deposit", "Withdrawal"]
        record_type = random.choice(types)

        yield [date_str, content, amount, record_type]


# Function to save the data to a CSV file and return its size
def save_to_csv(filename, data, current_file_size):
    with open(filename, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        if current_file_size == 0:
            csv_writer.writerow(["date", "content", "amount", "type"])
        csv_writer.writerows(data)

    return os.path.getsize(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_records", type=int, default=NUMBER_OF_RECORDS,
        help="Number of records to generate (default: 1000000)")

    args = parser.parse_args()

    directory = "./tests/data/"
    os.makedirs(directory, exist_ok=True)

    current_file_size = 0
    file_index = 0
    uuid = uuid4()
    filename = f"{directory}dummy_{uuid}.csv"

    print("Generating dummy data...")

    for record in generate_dummy_data(args.num_records):
        record_size = len(",".join(map(str, record))) + 1
        if current_file_size + record_size >= MAX_FILE_SIZE_MB * 1024 * 1024:
            print(f"Generated dummy data and saved to {filename}.")
            file_index += 1
            uuid = uuid4()
            filename = f"{directory}dummy_{uuid}.csv"
            current_file_size = 0

        save_to_csv(filename, [record], current_file_size)
        current_file_size += record_size

    print(f"Generated dummy data and saved to {file_index+1} files.")
