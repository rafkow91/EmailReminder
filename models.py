from collections import namedtuple
from datetime import datetime


class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def _is_valid_email(self):
        has_at = True if '@' in self.email else False
        has_dot_in_domain = True if '.' in self.email[-4:-2] else False

        return all([has_at, has_dot_in_domain])


class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author


class Hiring:
    def __init__(self, user: User, book: Book, returned_to: datetime) -> None:
        self.user = user
        self.book = book
        self.returned_to = returned_to

    def is_out_of_date(self):
        return datetime.now() > self.return_at
