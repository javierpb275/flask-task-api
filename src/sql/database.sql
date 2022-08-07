CREATE DATABASE flask_task_api;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(40) UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE tasks(
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(40) UNIQUE NOT NULL,
    description TEXT,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    user_id SERIAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);