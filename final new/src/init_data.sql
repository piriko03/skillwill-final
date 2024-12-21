PRAGMA foreign_keys = OFF;

-- Clean all tables without dropping them
DELETE FROM book_genres;
DELETE FROM book_authors;
DELETE FROM book_request;
DELETE FROM book;
DELETE FROM author;
DELETE FROM genre;
DELETE FROM user;

-- Reset SQLite sequences to ensure IDs start at 1
DELETE FROM sqlite_sequence;

PRAGMA foreign_keys = ON;


-- Now insert data in correct order without explicit IDs
INSERT INTO user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined,
                  location)
VALUES ('pbkdf2_sha256$870000$UWXAa026eUO7wOA5Z5gJlz$+1kygHX3XpcwwGzB+OGyL2/a2neObyUBAXOPcRBnrnw=',
        1, 'test', 'test', 'test', 'test@test.com', 0, 1, CURRENT_TIMESTAMP, 'Test City');

INSERT INTO author (name, biography)
VALUES ('Konstantine Gamsakhurdia', 'Georgian author'),
       ('Shota Rustaveli', 'Georgian author');

INSERT INTO genre (name, description)
VALUES ('Fantasy', 'Fantasy books');

INSERT INTO book (title, description, owner_id, status, pickup_location, created_at, updated_at)
VALUES ('Didostatis Marjvena', 'Fantasy novel', 1, 'available', 'Library', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Vepkhistkaosani', 'Fantasy novel', 1, 'available', 'Bookstore', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Link books to authors
INSERT INTO book_authors (book_id, author_id)
VALUES (1, 1),
       (2, 2);

-- Link books to genres
INSERT INTO book_genres (book_id, genre_id)
VALUES (1, 1),
       (2, 1);
