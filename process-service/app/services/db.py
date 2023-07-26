import csv
import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

load_dotenv()


class Importer:
    def __init__(
        self,
        db_name=os.getenv("POSTGRES_DB"),
        table_name=os.getenv("POSTGRES_TABLE"),
        db_user=os.getenv("POSTGRES_USER"),
        db_password=os.getenv("POSTGRES_PASSWORD"),
        db_host='postgres',
        db_port=5432
    ):
        self.db_name = db_name
        self.table_name = table_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def import_data(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def is_valid_format(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class CsvImporter(Importer):

    def is_valid_format(self, header) -> bool:
        expected_header = ["date", "content", "amount", "type"]
        return header == expected_header

    def import_data(self, csv_file_path=None) -> bool:
        if not csv_file_path:
            return False

        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)

            if not self.is_valid_format(header):
                return False

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
                f"COPY {self.table_name} ({', '.join(header)})"
                f"FROM STDIN WITH (FORMAT CSV, HEADER TRUE);"
            )
            cursor.copy_expert(copy_sql, f)

            conn.commit()
            cursor.close()
            conn.close()

        return True


# Now let's implement the XlsxImporter class

class XlsxImporter(Importer):

    def is_valid_format(self, header) -> bool:
        expected_header = ["date", "content", "amount", "type"]
        return header == expected_header

    def import_data(self, xlsx_file_path=None) -> bool:
        if not xlsx_file_path:
            return False

        df = pd.read_excel(xlsx_file_path)

        self.is_valid_format(df.columns.values.tolist())

        url = "postgresql://{}:{}@{}:{}/{}".format(
            self.db_user,
            self.db_password,
            self.db_host,
            self.db_port,
            self.db_name
        )

        engine = create_engine(url)

        df.to_sql(self.table_name, engine, if_exists='append', index=False)

        return True


class ImporterFactory:

    def __init__(self, file_path):
        self.file_path = file_path
        if file_path.endswith(".csv"):
            self.importer = CsvImporter()
        elif file_path.endswith(".xlsx"):
            self.importer = XlsxImporter()
        else:
            raise ValueError("Unknown file format")

    def import_data(self) -> bool:
        return self.importer.import_data(self.file_path)
