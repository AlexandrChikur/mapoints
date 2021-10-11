GET_POINT_QUERY = """
SELECT uid, name, x, y 
FROM points
WHERE uid = $1
"""

CREATE_POINT_QUERY = """
INSERT INTO points (uid, name, x, y) VALUES ($1, $2, $3, $4)
"""

GET_ALL_POINTS = """
SELECT * FROM points
"""
