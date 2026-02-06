
# Retorna un str que es:
# un insert a una tabla en lenguaje SQL
class InsertSQL:

    def __init__(self, colums: str, data: list | tuple): 
        self.colums = colums # Nombre de la tabla a la cúal insertar
        self.data = data # una tupla o lista de los datos que quiere insertar
        self.space = "" # inicializacion de los espacios de los datos
        self.isql = "INSERT INTO" # lenguaje sql

    # Retorna los espacios de los items en lenguaje SQL
    # Ej: VALUES (%s, %s, %s)
    def items_space(self):
        for i in range(int(len(self.data))-1):
            self.space += "%"+"s, "
        return f"VALUES ({self.space}%"+"s)" 

    # Retorna una consulta de SQL para hacer un insert
    #     Ej: INSERT INTO conversation ('id*', 'tile', 'time_start')
    #     VALUES (%s, %s, %s)
    def build(self):
        return f"{self.isql} {self.colums} {self.data} {self.items_space()}"


# Obtiene todos los mensajes de una conversacion concreta
# ordenados del más antiguo al más reciente
class SelectMessagesByConversation:
    SQL = """
    SELECT conversation_id, role, date, content
    FROM messages
    WHERE conversation_id = %s
    ORDER BY date ASC
    """


# Obtiene una conversación concreta según su id
class SelectConversationByIdSQL:
    SQL = """
    SELECT id, title, time_start
    FROM conversations
    WHERE id = %s
    """

if __name__ == "__main__":

    f = InsertSQL("messages", ("id_conversation", "role", "date", "content")).insert()
    print(f)