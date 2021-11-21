
CREATE TABLE IF NOT EXISTS public.points (
    uid UUID,
    name VARCHAR(24),
    x INT,
    y INT
);

CREATE TABLE IF NOT EXISTS public.users (
    id INT(12) PRIMARY KEY NOT NULL,
    username VARCHAR(16) NOT NULL,
    password VARCHAR(255) NOT NULL
);