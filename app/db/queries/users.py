CREATE_USER_QUERY = """
INSERT INTO public.users (username, password)
VALUES ($1, $2)
"""

CREATE_USER_QUERY_RETURNING_ID = """
INSERT INTO public.users (username, password)
VALUES ($1, $2)
RETURNING id
"""
GET_USER_BY_ID = """
SELECT id, username, password
FROM public.users
WHERE id = $1
"""

GET_USER_BY_USERNAME = """
SELECT id, username, password
FROM public.users
where username = $1

"""
