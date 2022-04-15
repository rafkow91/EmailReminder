import pytest
import sqlite3


""" Tests created by Adam Wójciński """
@pytest.fixture
def create_database():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE books
        (id integer, title text, author text, created_at date)
    ''')
    sample_data = [
        (1, 'Pan Samochodzik', 'Zbigniew Nienacki', '2020-01-02 13:59:16')
        (2, 'W pustyni i w puszczy', 'Henryk Sienkiewicz', '2019-02-13 11:59:16')
    ]
    cursor.executemany('INSERT INTO books VALUES(?, ?, ?, ?)', sample_data)
    return cursor

def test_get_data(create_database):
    pass