from faker import Faker
from controllers import Database

class BooksFactory:
    fake = Faker()

    def generate_books(self, quantity: int = 1):
        fake_data = []
        db = Database('database.db')
        
