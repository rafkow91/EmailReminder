""" Controllers """
from datetime import datetime
from sqlite3 import connect
from ssl import create_default_context
from smtplib import SMTP_SSL
from typing import Union
from dotenv import get_key

from models import Book, User, Hiring


class Database:
    """ class to manage db (sqlite)

    classes Book, User & Hiring are defined in module models.py
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.connection = connect(self.name)
        self.cursor = self.connection.cursor()

    def close_connection(self) -> None:
        """ method closes connection to db """
        self.cursor.close()

    def add_book(self, book: Book) -> None:
        """ method adds book to db

        Args:
            book (Book): class Book
        """
        data_to_add = (book.author, book.title, datetime.now())
        self.cursor.execute('''
            INSERT INTO books (author, title, created_at) VALUES (?, ?, ?)
        ''', data_to_add)
        self.connection.commit()

    def get_all_books(self) -> list:
        """ method returns all books from db

        Returns:
            list: list of objects type Book
        """
        self.cursor.execute('SELECT title, author FROM books')
        data = self.cursor.fetchall()
        result = []
        for row in data:
            result.append(Book(row[0], row[1]))
        return result

    def get_books_by_id(self, *books_ids) -> dict:
        """ method returns books

        Returns:
            dict: key is searched id, item is object type Book
        """
        result = {}
        for arg in books_ids:
            self.cursor.execute('''
                SELECT title, author FROM books WHERE id=?
            ''', (arg,))
            title, author = self.cursor.fetchone()
            result[arg] = Book(title, author)
        return result

    def get_books_by_author(self, *authors) -> dict:
        """ method returns books

        Returns:
            dict: key is searched author, item is list of objects type Book
        """
        result = {}
        for author in authors:
            self.cursor.execute('''
                SELECT title, author FROM books WHERE author LIKE ?
            ''', (author,))
            data = self.cursor.fetchall()
            book_list = []
            for row in data:
                book_list.append(Book(row[0], row[1]))
            result[author] = book_list
        return result

    def get_books_by_titles(self, *titles) -> dict:
        """ method returns books

        Returns:
            dict: key is searched title, item is list of objects type Book
        """
        result = {}
        for title in titles:
            self.cursor.execute('''
                SELECT title, author FROM books WHERE title LIKE ?
            ''', (f'%{title}%',))
            data = self.cursor.fetchall()
            book_list = []
            for row in data:
                book_list.append(Book(row[0], row[1]))
            result[title] = book_list
        return result

    def _get_book_id(self, book: Book) -> int:
        """ method returns book id

        Args:
            book (Book): object for which id is searched for

        Returns:
            int: searched book id, if book don't exist in db returns None
        """
        self.cursor.execute('''
            SELECT id FROM books WHERE author LIKE ? AND title LIKE ?
        ''', (book.author, book.title))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return None

    def add_user(self, user: User) -> None:
        """ method adds user to db

        Args:
            user (User): object type User
        """
        data_to_add = (user.name, user.email, datetime.now())
        self.cursor.execute('''
            INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)
        ''', data_to_add)
        self.connection.commit()

    def get_all_users(self) -> list:
        """ method returns all users from db

        Returns:
            list: list of objects type User
        """
        self.cursor.execute('SELECT name, email FROM users')
        data = self.cursor.fetchall()
        result = []
        for row in data:
            result.append(User(row[0], row[1]))
        return result

    def get_users_by_id(self, *users_ids) -> dict:
        """ method returns users

        Returns:
            dict: key is searched id, item is list of objects type User
        """
        result = {}
        for arg in users_ids:
            self.cursor.execute('''
                SELECT name, email FROM users WHERE id=?
            ''', (arg,))
            name, email = self.cursor.fetchone()
            result[arg] = User(name, email)
        return result

    def get_users_by_name(self, *users_names) -> dict:
        """ method returns users

        Returns:
            dict: key is searched name, item is list of objects type User
        """
        result = {}
        for name in users_names:
            self.cursor.execute('''
                SELECT name, email FROM users WHERE name LIKE ?
            ''', (f'%{name}%',))
            data = self.cursor.fetchall()
            user_list = []
            for row in data:
                user_list.append(User(row[0], row[1]))
            result[name] = user_list
        return result

    def _get_user_id(self, user: User) -> int:
        """ method returns user id

        Args:
            user (User): object for which id is searched for

        Returns:
            int: searched user id, if user don't exist in db returns None
        """
        self.cursor.execute('''
            SELECT id FROM users WHERE name LIKE ? AND email LIKE ?
        ''', (user.name, user.email))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return None

    def add_hiring(self, hiring: Hiring) -> None:
        """ method adds hiring to db

        Args:
            hiring (Hiring): object type Hiring
        """
        existing_hirings = self._get_all_hirings_id()

        user_id = self._get_user_id(hiring.user)
        book_id = self._get_book_id(hiring.book)

        if (book_id, user_id) not in existing_hirings:
            if user_id is None:
                self.add_user(hiring.user)
            if book_id is None:
                self.add_book(hiring.book)

            data_to_add = (user_id, book_id, datetime.now(), hiring.returned_to)

            self.cursor.execute('''
                INSERT INTO hirings (user_id, book_id, created_at, returned_to) VALUES (?, ?, ?, ?)
            ''', data_to_add)
            self.connection.commit()

    def get_all_hirings(self) -> list:
        """ method returns all hirings from db

        Returns:
            list: list of objects type Hiring
        """
        self.cursor.execute('''
        SELECT
            b.title, b.author,
            u.name, u.email,
            h.returned_to 
        FROM hirings h
        LEFT JOIN books b ON h.book_id=b.id
        LEFT JOIN users u ON h.user_id=u.id
        ''')

        data = self.cursor.fetchall()
        result = []

        for row in data:
            book = Book(row[0], row[1])
            user = User(row[2], row[3])
            returned_to = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            result.append(Hiring(user, book, returned_to))

        return result

    def _get_all_hirings_id(self) -> list:
        self.cursor.execute('SELECT book_id, user_id FROM hirings')

        return self.cursor.fetchall()


class EmailSender:
    """ class to manage sending emails """
    def __init__(self, env_path: str = '.env') -> None:
        self.env_path = env_path

        self.context = create_default_context()

        self.sender_name = get_key(self.env_path, 'sender_name')
        self.email = get_key(self.env_path, 'email')
        self.password = get_key(self.env_path, 'password')

        self.smtp_server = get_key(self.env_path, 'smtp_server')
        self.smtp_port = get_key(self.env_path, 'smtp_port')

    def send_email(self, reciver: str, message: Union[bytes, str]) -> None:
        """ method send email

        Args:
            reciver (str): email address of reciver
            message (Union[bytes, str]): message to send
        """
        with SMTP_SSL(self.smtp_server, self.smtp_port, context=self.context) as server:
            server.login(self.email, self.password)
            server.sendmail(from_addr=self.email, to_addrs=reciver, msg=message)

    def send_reminder_email(self, hiring: Hiring) -> None:
        """ method send reminder email

        Args:
            hiring (Hiring): object type Hiring which email is sended for
        """
        message = bytes(f'''
        From: {self.sender_name} <{self.email}>
        To: {hiring.user.name} <{hiring.user.email}>
        Subject: Czas zwrócić moją książkę

        Hej {hiring.user.name}!
        Może Ci umkneło, ale {hiring.returned_to.strftime('%d.%m.%Y')} powinieneś zwrócić moją książkę {hiring.book.title} (autorstwa {hiring.book.author})
        
        Będę wdzięczny za zwrot.

        Pozdrawiam,
        {self.sender_name}
        ''', encoding='utf8')

        self.send_email(hiring.user.email, message)
