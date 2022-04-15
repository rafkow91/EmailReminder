from datetime import datetime
from os import system, path, listdir
from sqlite3 import connect
from tabulate import tabulate
from time import sleep

from controllers import Database
from models import User, Book, Hiring


class Application:
    def __init__(self, database_name: str = 'database.db') -> None:
        self.database_name = database_name

        if not path.exists(self.database_name):
            self._create_empty_database()
            self._read_sql_scripts_from_database_dir()
            self._run_sql_scripts()

        self.database = Database(self.database_name)

    """ Procedures to create confirm database """

    def _create_empty_database(self):
        """ Create empty db file """
        open(self.database_name, mode='w').close()

    def _read_sql_scripts_from_database_dir(self):
        files_list = sorted(listdir('Database'))
        self.sql_commands = []

        for filename in files_list:
            with open(f'Database/{filename}', mode='r', encoding='utf8') as sql_script:
                lines = sql_script.readlines()
                lines = ' '.join(lines).split(';')
                for line in lines:
                    self.sql_commands.append(line)

    def _run_sql_scripts(self):
        connection = connect(self.database_name)
        cursor = connection.cursor()
        for command in self.sql_commands:
            cursor.execute(command)

    def _show_users(self):
        system('clear')
        print('Wykaz użytkowników')
        data = self.database.get_all_users()
        headers = ('Imię', 'Adres email')
        print(tabulate(data, headers=headers, tablefmt='fancy_grid', showindex=range(1, len(data)+1)))
        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _show_books(self):
        system('clear')
        print('Wykaz książek')
        data = self.database.get_all_books()
        headers = ('Tytuł', 'Autor')
        print(tabulate(data, headers=headers, tablefmt='fancy_grid', showindex=range(1, len(data)+1)))
        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _show_hirings(self):
        system('clear')
        print('Wykaz wypożyczeń')
        data = self.database.get_all_hirings()
        headers = ('Tytuł', 'Autor', 'Wypożyczający', 'Data zwrotu')
        print(tabulate(data, headers=headers, tablefmt='fancy_grid', showindex=range(1, len(data)+1)))
        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _add_user(self):
        system('clear')
        print('Wykaz wypożyczeń')
        

    def _add_book(self):
        system('clear')
        print('Wykaz wypożyczeń')
        

    def _add_hiring(self):
        system('clear')
        print('Dodaj nowe wypożyczenie\n\nWypożyczający:')
        
        username = input('Imię: ')
        existed_users = self.database.get_users_by_name(username)
                
        if existed_users[username] is None:
            email = input('Adres email: ')
            self.database.add_user(User(username, email))
        
        user_id = self.database.get_users_by_name(username)[username][0]

        print('Książka:')
        title = input('Tytuł: ')
        existed_books = self.database.get_books_by_titles(title)[title]
        data = [row[1:3] for row in existed_books]
        print(f'Znaleziono {len(existed_books)} książek o tytule zawierającym frazę "{title}"')
        headers = ('Tytuł', 'Autor')
        print(tabulate(data, headers=headers, tablefmt='fancy_grid', showindex=range(1, len(data)+1)))
        print('\n\n')
        while True:
            try:
                choice = int(input('Wybierz, którą książkę chcesz wypożyczyć: '))
                if choice not in range(len(existed_books)):
                    raise ValueError
            except ValueError:
                print('!!! Wybrano złą wartość !!!')
                continue
            break
        book_id = existed_books[choice - 1][0]
        print('Podaj datę zwrotu:')
        day = int(input('Dzień: '))
        month = int(input('Miesiąc (0 - 12): '))
        year = int(input('Rok: '))
        returned_to = datetime(year, month, day)
        hiring = Hiring()

    def run(self):
        OPTIONS = {
            1: self._show_users,
            2: self._show_books,
            3: self._show_hirings,
            4: self._add_book,
            5: self._add_user,
            6: self._add_hiring,
            0: self.quit_app
        }

        system('clear')
        print('''Witaj w menadżerze wypożyczania książek
    
        Dostępne opcje:
    1 - pokaż wszystkich wypożyczających
    2 - pokaż wszystkie książki
    3 - pokaż wszystkie wypożyczenia

    4 - dodaj wypożyczającego
    5 - dodaj książkę
    6 - dodaj wypożyczenie
    
    0 - wyjście
    
    ''')
        while True:
            try:
                choice = int(input('Wybierz co chcesz zrobić: '))
                if choice not in range(len(OPTIONS)):
                    raise ValueError
            except ValueError:
                print('\t!!! Wybierz odpowiednią liczbę !!!')
                continue
            break

        OPTIONS[choice]()
        

    def quit_app(self):
        system('clear')
        print('Do zobaczenia :)')
        sleep(2)
        system('clear')
