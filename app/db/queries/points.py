GET_POINT_QUERY_BY_ID = """
SELECT id, name, x, y, user_id
FROM points
WHERE id = $1
"""

DELETE_POINT_QUERY_BY_ID = """
DELETE FROM points
WHERE points.id = $1
"""

GET_POINTS_QUERY_BY_USER_ID = """
SELECT id, name, x, y, user_id
FROM points
WHERE user_id = $1
"""

CREATE_POINT_QUERY = """
INSERT INTO points (name, x, y, user_id) VALUES ($1, $2, $3, $4)
"""

CREATE_POINT_QUERY_RETURNING_ID = """
INSERT INTO points (name, x, y, user_id) VALUES ($1, $2, $3, $4) RETURNING id
"""

GET_ALL_POINTS = """
SELECT * FROM points
"""

GET_ALL_POINTS_IDS = """
SELECT id
FROM points
"""

GET_ALL_USER_POINTS = """
SELECT * FROM points WHERE user_id = $1
"""

GET_ALL_USER_POINTS_IDS = """
SELECT id
FROM points
WHERE user_id = $1
"""
