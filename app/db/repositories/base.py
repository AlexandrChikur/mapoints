from asyncpg.connection import Connection


class BaseRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn
        
    @property
    def conntection(self) -> Connection:
        return self._conn