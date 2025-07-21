use `library_db`;
-- Tabulka autorů
CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT,
    nationality VARCHAR(100)
);

-- Tabulka knih
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT,
    isbn VARCHAR(13),
    year_published INT,
    genre VARCHAR(100),
    available_copies INT DEFAULT 0,
    total_copies INT DEFAULT 0,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

-- Tabulka výpůjček
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    borrower_name VARCHAR(255) NOT NULL,
    borrower_email VARCHAR(255),
    loan_date DATE,
    return_date DATE,
    returned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Vložení autorů
INSERT INTO authors (name, birth_year, nationality) VALUES
('J.K. Rowling', 1965, 'British'),
('George Orwell', 1903, 'British'),
('Agatha Christie', 1890, 'British'),
('Isaac Asimov', 1920, 'American'),
('Terry Pratchett', 1948, 'British'),
('Stephen King', 1947, 'American');

-- Vložení knih
INSERT INTO books (title, author_id, isbn, year_published, genre, available_copies, total_copies) VALUES
('Harry Potter and the Philosopher''s Stone', 1, '9780747532699', 1997, 'Fantasy', 2, 5),
('Harry Potter and the Chamber of Secrets', 1, '9780747538493', 1998, 'Fantasy', 1, 3),
('1984', 2, '9780451524935', 1949, 'Dystopian Fiction', 0, 4),
('Animal Farm', 2, '9780451526342', 1945, 'Political Satire', 3, 4),
('Murder on the Orient Express', 3, '9780062693662', 1934, 'Mystery', 1, 2),
('The Poirot Investigations', 3, '9780006499824', 1924, 'Mystery', 2, 3),
('Foundation', 4, '9780553293357', 1951, 'Science Fiction', 1, 2),
('I, Robot', 4, '9780553294385', 1950, 'Science Fiction', 0, 3),
('The Colour of Magic', 5, '9780552166591', 1983, 'Fantasy', 2, 2),
('The Shining', 6, '9780307743657', 1977, 'Horror', 0, 2);

-- Vložení půjčených knih (aktuálně vypůjčené)
INSERT INTO loans (book_id, borrower_name, borrower_email, loan_date, return_date, returned) VALUES
-- Vypůjčené knihy (returned = FALSE)
(1, 'Jan Novák', 'jan.novak@email.cz', '2024-07-01', '2024-07-15', FALSE),
(1, 'Marie Svobodová', 'marie.svoboda@email.cz', '2024-07-05', '2024-07-19', FALSE),
(1, 'Petr Dvořák', 'petr.dvorak@email.cz', '2024-07-10', '2024-07-24', FALSE),
(2, 'Anna Nováková', 'anna.novakova@email.cz', '2024-07-08', '2024-07-22', FALSE),
(2, 'Tomáš Procházka', 'tomas.prochazka@email.cz', '2024-07-12', '2024-07-26', FALSE),
(3, 'Lucie Černá', 'lucie.cerna@email.cz', '2024-06-20', '2024-07-04', FALSE),
(3, 'David Svoboda', 'david.svoboda@email.cz', '2024-06-25', '2024-07-09', FALSE),
(3, 'Eva Horáková', 'eva.horakova@email.cz', '2024-07-01', '2024-07-15', FALSE),
(3, 'Martin Krejčí', 'martin.krejci@email.cz', '2024-07-08', '2024-07-22', FALSE),
(5, 'Petra Maršálková', 'petra.marsalkova@email.cz', '2024-07-15', '2024-07-29', FALSE),
(8, 'Jakub Veselý', 'jakub.vesely@email.cz', '2024-07-02', '2024-07-16', FALSE),
(8, 'Klára Bendová', 'klara.bendova@email.cz', '2024-07-07', '2024-07-21', FALSE),
(8, 'Ondřej Šťastný', 'ondrej.stastny@email.cz', '2024-07-14', '2024-07-28', FALSE),
(10, 'Tereza Kratochvílová', 'tereza.kratochvilova@email.cz', '2024-06-28', '2024-07-12', FALSE),
(10, 'Michal Pokorný', 'michal.pokorny@email.cz', '2024-07-03', '2024-07-17', FALSE),

-- Již vrácené knihy (returned = TRUE)
(1, 'Zuzana Krásná', 'zuzana.krasna@email.cz', '2024-06-01', '2024-06-15', TRUE),
(2, 'Pavel Novotný', 'pavel.novotny@email.cz', '2024-06-05', '2024-06-19', TRUE),
(4, 'Lenka Moravcová', 'lenka.moravcova@email.cz', '2024-06-10', '2024-06-24', TRUE),
(6, 'Roman Štěpánek', 'roman.stepanek@email.cz', '2024-06-15', '2024-06-29', TRUE),
(7, 'Barbora Kadlecová', 'barbora.kadlecova@email.cz', '2024-06-20', '2024-07-04', TRUE),
(9, 'Filip Černý', 'filip.cerny@email.cz', '2024-06-25', '2024-07-09', TRUE);