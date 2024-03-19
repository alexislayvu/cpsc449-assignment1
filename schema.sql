-- create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS job_board;

-- use the database
USE job_board;

-- create the jobs table
CREATE TABLE
    IF NOT EXISTS jobs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        company VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL
    );

-- insert sample data into the jobs table
INSERT INTO
    jobs (title, company, location)
VALUES
    (
        'Software Engineer',
        'Google',
        'Mountain View, CA'
    ),
    ('Marketing Specialist', 'Apple', 'Cupertino, CA'),
    ('Data Analyst', 'Amazon', 'Seattle, WA');