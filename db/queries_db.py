class PSQL:

    def __init__(self, curr, conn):

        # Verificar que curr sea un cursor valido
        if not hasattr(curr, "execute"):
            raise TypeError("curr must be a database cursor")
        
        # Verificar que conn sea una conexión valida
        if not hasattr(conn, "commit"):
            raise TypeError("conn must be a database connection")

        # Cursor sql
        self.curr = curr
        # conección sql
        self.conn = conn


class ExecutePSQL(PSQL):

    # Hace la querie si la querie requiere sql y datos
    def act(self,sql:str,data:tuple | list):
        self.curr.execute(
            sql,
            data
        )

class CommitPSQL(PSQL):

    # Guarda los datos en la db haciendo un commit
    def act(self):
        self.conn.commit()
