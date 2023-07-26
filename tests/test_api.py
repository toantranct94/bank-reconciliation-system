import base64
import os

import psycopg2
import pytest
import requests

BASE_URL = 'http://localhost:8080/api/'
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
POSTGRES_USER = 'admin'
POSTGRES_PASSWORD = 'admin'
POSTGRES_DB = 'test'
POSTGRES_TABLE = 'transactions'
NUMBER_OF_RECORDS = 1000000


@pytest.fixture
def access_token():
    credentials = base64.b64encode(
        f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    response = requests.post(
        BASE_URL + 'auth/token',
        headers={'Authorization': f'Basic {credentials}'})
    assert response.status_code == 200
    token = response.json().get('token', None)
    return token


@pytest.fixture
def folder():
    credentials = base64.b64encode(
        f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    response = requests.post(
        BASE_URL + 'auth/token',
        headers={'Authorization': f'Basic {credentials}'})
    token = response.json().get('token', None)
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(BASE_URL + 'upload', headers=headers)
    assert response.status_code == 200
    folder = response.json().get('folder', None)
    return folder


@pytest.fixture
def db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    yield conn
    conn.close()


def get_csv_files(folder_path):
    # Get a list of CSV files in the folder
    csv_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(folder_path, file))
    return csv_files


def upload_csv_file(folder, token, file_path):
    # Upload a single CSV file using the API call
    files = {'file': open(file_path, 'rb')}
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.post(
        BASE_URL + f'upload/{folder}', files=files, headers=headers)
    return response


def test_token_retrieval(access_token):
    assert access_token is not None


def test_create_folder(folder):
    assert folder is not None


def test_upload_files(access_token, folder):
    folder_path = './tests/data'
    csv_files = get_csv_files(folder_path)

    for file_path in csv_files:
        response = upload_csv_file(folder, access_token, file_path)
        assert response.status_code == 200, f"Failed to upload: {file_path}"


def test_get_transactions(db_connection):
    # Call the function being tested
    cursor = db_connection.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM {POSTGRES_TABLE};')
    count = cursor.fetchone()[0]
    # Perform assertions
    assert count >= NUMBER_OF_RECORDS
