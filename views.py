""" definition of all views used in app """
from datetime import datetime
from os import system, path, listdir
from sqlite3 import connect
from time import sleep
from tabulate import tabulate

from controllers import Database, EmailSender
from models import User, Book, Hiring


class Application:
    """ main class of application """

    def __init__(self, database_name: str = 'database.db'):
        self.database_name = database_name

        if not path.exists(self.database_name):
            self._create_empty_database()
            self._read_sql_scripts_from_database_dir()
            self._run_sql_scripts()

        self.database = Database(self.database_name)

    def _create_empty_database(self):
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
        data = [(user.name, user.email) for user in self.database.get_all_users()]
        headers = ('Imię', 'Adres email')

        print(tabulate(
            data, headers=headers,
            tablefmt='fancy_grid',
            showindex=range(1, len(data)+1)))

        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _show_books(self):
        system('clear')
        print('Wykaz książek')
        data = [(book.title, book.author) for book in self.database.get_all_books()]
        headers = ('Tytuł', 'Autor')

        print(tabulate(
            data, headers=headers,
            tablefmt='fancy_grid',
            showindex=range(1, len(data)+1)))

        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _show_hirings(self):
        system('clear')
        print('Wykaz wypożyczeń')

        data = [(hiring.book.title,
                hiring.book.author,
                hiring.user.name,
                hiring.returned_to.strftime('%Y-%m-%d'))
                for hiring in self.database.get_all_hirings()]
        headers = ('Tytuł', 'Autor', 'Wypożyczający', 'Data zwrotu')

        print(tabulate(
            data, headers=headers,
            tablefmt='fancy_grid',
            showindex=range(1, len(data)+1)))

        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _add_user(self):
        system('clear')
        print('Dodaj nowego wypożyczającego')
        username = input('Imię: ')
        email = input('Adres email: ')

        existed_users = self.database.get_all_users()
        if (username, email) not in existed_users:
            self.database.add_user(user=User(username, email))

        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _add_book(self):
        system('clear')
        print('Dodaj nową książkę do wypożyczania')
        title = input('Tytuł: ')
        author = input('Autor: ')

        existed_books = self.database.get_all_books()
        if (title, author) not in existed_books:
            self.database.add_book(book=Book(title, author))

        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def _add_hiring(self):
        system('clear')
        print('Dodaj nowe wypożyczenie\n\n\tWypożyczający:')

        username = input('Imię: ')
        existed_users = self.database.get_users_by_name(username)[username]

        if len(existed_users) > 1:
            data = [(user.name, user.email) for user in existed_users]
            print(f'Znaleziono {len(existed_users)} ' +
                  f'użytkowników o nazwie zawierającej frazę "{username}"')
            headers = ('Imię', 'Adres email')

            print(tabulate(
                data, headers=headers,
                tablefmt='fancy_grid',
                showindex=range(1, len(data)+1)))

            print('\n\n')
            while True:
                try:
                    choice = int(input('Wybierz wypożyczającego (naciśnij 0 aby dodać nowego): '))
                    if choice == 0:
                        self._add_user()
                    elif choice not in range(len(existed_users)):
                        raise ValueError
                except ValueError:
                    print('!!! Wybrano złą wartość !!!')
                    continue
                break
        else:
            choice = 1
        try:
            email = existed_users[choice - 1].email
        except IndexError:
            email = input('Adres email: ')
            self.database.add_user(User(username, email))

        user = User(username, email)

        print('\tKsiążka:')
        title = input('Tytuł: ')
        existed_books = self.database.get_books_by_titles(title)
        existed_books = existed_books[title]
        data = [(book.title, book.author) for book in existed_books]
        if len(data) > 1:
            print(f'Znaleziono {len(existed_books)} książek o tytule zawierającym frazę "{title}"')
            headers = ('Tytuł', 'Autor')

            print(tabulate(
                data, headers=headers,
                tablefmt='fancy_grid',
                showindex=range(1, len(data)+1)))

            print('\n\n')
            while True:
                try:
                    choice = int(input('Wybierz, którą książkę chcesz wypożyczyć (aby dodać nową wybierz 0): '))
                    if choice == 0:
                        self._add_book()
                    elif choice not in range(len(existed_books)):
                        raise ValueError
                except ValueError:
                    print('!!! Wybrano złą wartość !!!')
                    continue
                break
            title = existed_books[choice - 1].title
            author = existed_books[choice - 1].author

        else:
            print('Nie znaleziono książki o podobnym tytule. Dodaj taką książkę:')
            title = input('Tytuł: ')
            author = input('Autor: ')

        book = Book(title, author)

        print('Podaj datę zwrotu:')
        day = int(input('Dzień: '))
        month = int(input('Miesiąc (0 - 12): '))
        year = int(input('Rok: '))
        returned_to = datetime(year, month, day)

        self.database.add_hiring(
            Hiring(user, book, returned_to)
        )
        self.run()

    def _send_reminder_emails(self):
        sender = EmailSender()

        system('clear')
        print('Wysyłanie maili z przypomnieniem\n')
        for hiring in self.database.get_all_hirings():
            if hiring.is_out_of_date():
                if hiring.user.is_valid_email():
                    sender.send_reminder_email(hiring)
                    print(f'Wysłano mail do: {hiring.user}')
                else:
                    print(f'Nie udało się wysłać maila do {hiring.user} - niepoprawny adres email!')

        input('\n\n--- Naciśnij dowolny klawisz aby kontynuować ---\n\n')
        self.run()

    def run(self):
        OPTIONS = {
            1: self._show_users,
            2: self._show_books,
            3: self._show_hirings,
            4: self._add_user,
            5: self._add_book,
            6: self._add_hiring,
            7: self._send_reminder_emails,
            0: self.quit_app,
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

    7 - wyślij maile z przypomnieniem o zwrocie przetrzymanych książek
    
    0 - wyjście
    
    ''')
        while True:
            try:
                choice = int(input('Wybierz co chcesz zrobić: '))
                if choice not in OPTIONS:
                    raise ValueError
            except ValueError:
                print('\t!!! Wybierz odpowiednią liczbę !!!')
                continue
            break

        OPTIONS[choice]()

    @staticmethod
    def quit_app():
        """ Close app """
        system('clear')
        print('Do zobaczenia :)')
        sleep(1)
        system('clear')
