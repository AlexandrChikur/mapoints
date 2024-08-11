GET_POINT_QUERY_BY_ID = """
SELECT points.id, points.name, points.x, points.y, points.user_id, users.username as author_name
FROM points
INNER JOIN users ON points.user_id = users.id
WHERE points.id = $1
"""

DELETE_POINT_QUERY_BY_ID = """
DELETE FROM points
WHERE points.id = $1
"""

GET_POINTS_QUERY_BY_USER_ID = """
SELECT points.id, points.name, points.x, points.y, points.user_id, users.username as author_name
FROM points
INNER JOIN users ON points.user_id = users.id
WHERE points.user_id = $1
"""

CREATE_POINT_QUERY = """
INSERT INTO points (name, x, y, user_id) VALUES ($1, $2, $3, $4)
"""

CREATE_POINT_QUERY_RETURNING_ID = """
INSERT INTO points (name, x, y, user_id) VALUES ($1, $2, $3, $4) RETURNING id
"""

CREATE_POINT_INCREMENT_QUERY = """ 
UPDATE users SET points_amount = points_amount + 1 WHERE users.id = $1
"""

CREATE_POINT_DECREMENT_QUERY = """ 
UPDATE users SET points_amount = points_amount - 1 WHERE users.id = $1
"""

GET_ALL_POINTS = """
SELECT points.id, points.name, points.x, points.y, points.user_id, users.username as author_name
FROM points
INNER JOIN users ON points.user_id = users.id
"""

GET_ALL_POINTS_LOOKUP = """
SELECT points.id, points.name, points.x, points.y, points.user_id, users.username as author_name
FROM points
INNER JOIN users ON points.user_id = users.id
WHERE points.name LIKE $1
    OR users.username LIKE $1
"""

GET_ALL_POINTS_IDS = """
SELECT id
FROM points
"""

GET_ALL_USER_POINTS = """
SELECT points.id, points.name, points.x, points.y, points.user_id, users.username as author_name
FROM points 
INNER JOIN users ON points.user_id = users.id
WHERE user_id = $1
"""

GET_ALL_USER_POINTS_IDS = """
SELECT id
FROM points
WHERE user_id = $1
"""