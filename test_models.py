from datetime import datetime
from models import User, Book, Hiring

user = User('user', 'test@mail.com')
book = Book('book', 'author')


def test_is_out_of_date():
    hiring1 = Hiring(user, book, datetime(2000, 1, 1))
    assert hiring1.is_out_of_date() == True

    hiring2 = Hiring(user, book, datetime(3000, 1, 1))
    assert hiring2.is_out_of_date() == False


def test_is_valid_email():
    assert user._is_valid_email() == True

    user.email = 'test'
    assert user._is_valid_email() == False

    user.email = 'test@abc'
    assert user._is_valid_email() == False

    user.email = 'test@abc.pl'
    assert user._is_valid_email() == True
