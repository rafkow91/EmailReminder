""" definition of all models used in app """
from datetime import datetime


class User:
    """ class defines user (including name and email)"""
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f'{self.name} ({self.email})'

    def is_valid_email(self) -> bool:
        """ method checks if email is valid:
            - contains '@'
            - contains '.' on 3rd or 4th position from the end

        Returns:
            bool
        """
        has_at = bool('@' in self.email)
        has_dot_in_domain = bool('.' in self.email[-4:-2])

        return all([has_at, has_dot_in_domain])


class Book:
    """ class defines book (including title and author)"""
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author

    def __repr__(self) -> str:
        return f'{self.author}: "{self.title}"'


class Hiring:
    """ class defines hiring (including user, book and time to returned)"""
    def __init__(self, user: User, book: Book, returned_to: datetime) -> None:
        self.user = user
        self.book = book
        self.returned_to = returned_to

    def is_out_of_date(self) -> bool:
        """ method checks if book is out of date

        Returns:
            bool
        """
        return datetime.now() > self.returned_to
