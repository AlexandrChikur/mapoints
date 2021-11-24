
CREATE TABLE IF NOT EXISTS public.points (
    uid UUID,
    name VARCHAR(24),
    x INT,
    y INT
);

CREATE TABLE IF NOT EXISTS public.users (
    id BIGINT PRIMARY KEY NOT NULL DEFAULT (nextval('seqUsers')),
    username VARCHAR(16) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);