from uuid import UUID

# Retorna un str que es:
# un insert a una tabla en lenguaje SQL
class InsertSQL:

    def __init__(self, table: str, columns: tuple): 
        self.table = table # Nombre de la tabla a la cúal insertar
        self.columns = columns # una tupla o lista de los datos que quiere insertar
 
    # Retorna una consulta de SQL para hacer un insert
    #     Ej: INSERT INTO conversation ('id*', 'tile', 'time_start')
    #     VALUES (%s, %s, %s)
    def build(self):
        cols = ", ".join(self.columns)
        placeholders = ", ".join(["%s"] * len(self.columns))
        return f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"


# Obtiene todos los mensajes de una conversacion concreta
# ordenados del más antiguo al más reciente
class SelectMessagesByConversation:
    SQL = """
    SELECT id_conversation, role, date, content
    FROM messages
    WHERE id_conversation = %s
    ORDER BY date ASC
    """


# Obtiene una conversación concreta según su id
class SelectConversationByIdSQL:
    SQL = """
    SELECT id, title, time_start, behavior
    FROM conversations
    WHERE id = %s
    """

class SelectConversationSQL:
    SQL = """
    SELECT id, title, time_start, behavior
    FROM conversations
    """

class UpDateConversationsSQL:

    def __init__(self, col):
        
        # Valida que col sea un str
        if not isinstance(col, str):
            raise TypeError("col must be a string")
        # Valida que col no esté vacío
        if not col.strip():
            raise ValueError("col cannot be empty")

        self.col = col
        
    def build(self):    
        return f"""
    UPDATE conversations
    SET {self.col} = %s
    WHERE id = %s
    """


if __name__ == "__main__":

    f = InsertSQL("messages", ("id_conversation", "role", "date", "content")).build()
    print(f)