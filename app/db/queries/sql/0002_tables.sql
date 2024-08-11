

CREATE TABLE IF NOT EXISTS public.users (
    id BIGINT PRIMARY KEY NOT NULL DEFAULT (nextval('seqUsers')),
    username VARCHAR(16) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    points_amount INT DEFAULT 0,
    CONSTRAINT valid_number
        check (points_amount <= 10)
);

CREATE TABLE IF NOT EXISTS public.points (
    id INT PRIMARY KEY NOT NULL DEFAULT (nextval('seqPoints')),
    name VARCHAR(24),
    x INT,
    y INT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES public.users (id)
);