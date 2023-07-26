import csv
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()


class CsvToPostgresImporter:
    def __init__(
        self,
        db_name=os.getenv("POSTGRES_DB"),
        table_name=os.getenv("POSTGRES_TABLE"),
        db_user=os.getenv("POSTGRES_USER"),
        db_password=os.getenv("POSTGRES_PASSWORD"),
        db_host='postgres',
        db_port=5432
    ):
        self.csv_file = None
        self.db_name = db_name
        self.table_name = table_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def set_file(self, csv_file):
        self.csv_file = csv_file

    def import_data(self):
        if not self.csv_file:
            return
        with open(self.csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            columns = next(reader)
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Use the COPY command to efficiently import data to PostgreSQL
            copy_sql = (
                f"COPY {self.table_name} ({', '.join(columns)})"
                f"FROM STDIN WITH (FORMAT CSV, HEADER TRUE);"
            )
            cursor.copy_expert(copy_sql, csvfile)

            conn.commit()
            cursor.close()
            conn.close()


# if __name__ == "__main__":
#     csv_file_path = "path/to/your/csv_file.csv"
#     db_name = "your_db_name"
#     table_name = "your_table_name"
#     db_user = "your_db_user"
#     db_password = "your_db_password"

#     importer = CsvToPostgresImporter(
#         csv_file_path, db_name, table_name, db_user, db_password)
#     importer.import_data()
