

GET_POINT_QUERY = """
SELECT uid, x, y 
FROM points
WHERE uid = $1
"""

CREATE_POINT_QUERY = """
INSERT INTO points (uid, x, y) VALUES ($1, $2, $3)
"""