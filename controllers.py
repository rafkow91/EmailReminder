from sqlite3 import connect
from datetime import datetime

from models import Book, User, Hiring


class Database:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connection = connect(self.name)
        self.cursor = self.connection.cursor()

    def close_connection(self) -> None:
        self.cursor.close()

    def add_book(self, book: Book) -> None:
        data_to_add = (book.author, book.title, datetime.now())
        self.cursor.execute('''
            INSERT INTO books (author, title, created_at) VALUES (?, ?, ?)
        ''', data_to_add)
        self.connection.commit()

    def get_all_books(self) -> list:
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()

    def get_books_by_id(self, *books_ids) -> dict:
        result = {}
        for arg in books_ids:
            self.cursor.execute('''
                SELECT * FROM books WHERE id=?
            ''', (arg,))
            result[arg] = self.cursor.fetchone()
        return result

    def get_books_by_author(self, *authors) -> dict:
        result = {}
        for author in authors:
            self.cursor.execute('''
                SELECT * FROM books WHERE author LIKE ?
            ''', (author,))
            result[author] = self.cursor.fetchall()
        return result

    def add_user(self, user: User) -> None:
        data = self.get_all_users()
        usernames = [data[i][1].lower() for i in range(len(data))]
        emails = [data[i][2].lower() for i in range(len(data))]
        if user.name.lower() not in usernames or user.email.lower() not in emails:
            data_to_add = (user.name, user.email, datetime.now())
            self.cursor.execute('''
                INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)
            ''', data_to_add)
            self.connection.commit()

    def get_all_users(self) -> list:
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def add_hiring(self, hiring: Hiring) -> None:
        data_to_add = (hiring.user.name, hiring.book.title, datetime.now())
        self.cursor.execute('''
            INSERT INTO books (author, title, created_at) VALUES (?, ?, ?)
        ''', data_to_add)
        self.connection.commit()

    def get_all_hirings(self) -> list:
        self.cursor.execute('SELECT * FROM hirings')
        return self.cursor.fetchall()
