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
        self.cursor.execute('SELECT title, author FROM books')
        return self.cursor.fetchall()

    def get_books_by_id(self, *books_ids) -> dict:
        result = {}
        for arg in books_ids:
            self.cursor.execute('''
                SELECT title, author FROM books WHERE id=?
            ''', (arg,))
            result[arg] = self.cursor.fetchone()
        return result

    def get_books_by_author(self, *authors) -> dict:
        result = {}
        for author in authors:
            self.cursor.execute('''
                SELECT title, author FROM books WHERE author LIKE ?
            ''', (author,))
            result[author] = self.cursor.fetchall()
        return result

    def get_books_by_titles(self, *titles) -> dict:
        result = {}
        for title in titles:
            self.cursor.execute('''
                SELECT * FROM books WHERE title LIKE ?
            ''', (f'%{title}%',))
            result[title] = self.cursor.fetchall()
        return result

    def _get_book_id(self, book: Book) -> int:
        self.cursor.execute('''
            SELECT id FROM books WHERE author LIKE ? AND title LIKE ?
        ''', (book.author, book.title))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return None

    def add_user(self, user: User) -> None:
        data_to_add = (user.name, user.email, datetime.now())
        self.cursor.execute('''
            INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)
        ''', data_to_add)
        self.connection.commit()

    def get_all_users(self) -> list:
        self.cursor.execute('SELECT name, email FROM users')
        return self.cursor.fetchall()

    def get_users_by_id(self, *users_ids) -> dict:
        result = {}
        for arg in users_ids:
            self.cursor.execute('''
                SELECT name, email FROM users WHERE id=?
            ''', (arg,))
            result[arg] = self.cursor.fetchone()
        return result

    def get_users_by_name(self, *users_names) -> dict:
        result = {}
        for name in users_names:
            self.cursor.execute('''
                SELECT * FROM users WHERE name LIKE ?
            ''', (f'%{name}%',))
            result[name] = self.cursor.fetchall()
        return result

    def _get_user_id(self, user: User) -> int:
        self.cursor.execute('''
            SELECT id FROM users WHERE name LIKE ? AND email LIKE ?
        ''', (user.name, user.email))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return None

    def add_hiring(self, hiring: Hiring) -> None:
        existing_hirings = self._get_all_hirings_id()
        
        user_id = self._get_user_id(hiring.user)
        book_id = self._get_book_id(hiring.book)

        if (book_id, user_id) not in existing_hirings:
            if user_id is None:
                self.add_user(hiring.user)
            if book_id is None:
                self.add_book(hiring.book)

            data_to_add = (user_id, book_id, datetime.now(), hiring.return_at)

            self.cursor.execute('''
                INSERT INTO hirings (user_id, book_id, created_at, returned_to) VALUES (?, ?, ?, ?)
            ''', data_to_add)
            self.connection.commit()

    def get_all_hirings(self) -> list:
        self.cursor.execute('SELECT book_id, user_id, returned_to FROM hirings')

        data = self.cursor.fetchall()
        result = []

        for row in data:
            book = self.get_books_by_id(row[0])
            user = self.get_users_by_id(row[1])
            returned_to = row[2]
            to_add = (book[row[0]][0], book[row[0]][1], user[row[1]][0], returned_to)
            result.append(to_add)

        return result

    def _get_all_hirings_id(self) -> list:
        self.cursor.execute('SELECT book_id, user_id FROM hirings')

        return self.cursor.fetchall()
