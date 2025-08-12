-- SQLite
SELECT * FROM users
WHERE username in ('Miza', 'Lucas', 'Nicolas')

DELETE FROM users
WHERE username not in ('Miza', 'Lucas', 'Nicolas')