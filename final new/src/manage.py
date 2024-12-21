import os
import sys
from django.core.management import execute_from_command_line
from django.db import connection, OperationalError
import shutil


def init_data():
    required_tables = ['user', 'author', 'genre', 'book', 'book_request', 'book_authors', 'book_genres']
    try:
        with connection.cursor() as cursor:
            # Verify all required tables exist
            for table in required_tables:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=%s", [table])
                if cursor.fetchone() is None:
                    print(f"Error: Required table '{table}' does not exist. Migrations may have failed.")
                    sys.exit(1)

        # All tables exist, load data
        with open('init_data.sql', 'r') as file:
            sql_script = file.read()
            with connection.cursor() as cursor:
                cursor.executescript(sql_script)
        print("Initial data loaded successfully.")

    except OperationalError as e:
        print(f"Error loading initial data: {e}")
        sys.exit(1)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    try:
        # Drop database and migrations
        if len(sys.argv) > 1 and sys.argv[1] == 'dropall':
            if os.path.exists('db.sqlite3'):
                os.remove('db.sqlite3')

            migrations_dirs = ['users/migrations', 'books/migrations']
            for dir in migrations_dirs:
                if os.path.exists(dir):
                    shutil.rmtree(dir)
                os.makedirs(dir)
                with open(f'{dir}/__init__.py', 'w') as f:
                    pass

            print("Dropped database and migrations.")
            return

        # Runserver logic
        if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
            # Ensure migrations are applied
            execute_from_command_line(['manage.py', 'makemigrations', 'books', 'users'])
            execute_from_command_line(['manage.py', 'migrate'])

            # Load initial data
            init_data()

            # Start the server
            execute_from_command_line(['manage.py', 'runserver'])
            return

    except IndexError:
        pass

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
