from db.sql_language import (
    InsertSQL,
    SelectConversationByIdSQL,
    UpDateConversationsSQL
)
from db.models_db import ConversationSQLMapper
 

# manejará las principales funciones de la tabla conversation
class ConversationRepository:

    # Se le tendrá que pasar una conexion
    # de la base de datos
    def __init__(self, db, data):
        self.db = db
        self.data = data
 
    # Crea una fila en conversation
    def create(self, conversation: ConversationSQLMapper):
        # Usa InsertSQL para crea una consulta sql
        # mas concretamente un insert. más o menos como este:
        #     INSERT INTO conversation (id*, tile, time_start, behavior)
        #     VALUES (%s, %s, %s)
        sql = InsertSQL(
            table="conversations",
            columns=conversation.COLUMNS
        ).build()

        # Hace la consulta sql
        # conversation.to_row() = datos de la conversación
        self.db.cur.execute(sql, conversation.to_row(self.data))

    # Obtener una conversación según su id
    # tenemos que pasarle el id de alguna conversación
    def get_by_id(self, conversation_id):
        # Obtenemos el sql
        # mas concretamente un SELECT como este:
        #    SELECT id, title, time_start, behavior
        #    FROM conversations
        #    WHERE id = %s
        sql = SelectConversationByIdSQL().SQL

        # Hace la consulta sql
        # conversation_id = el id de alguna conversación
        self.db.cur.execute(sql, (conversation_id,))

        # Devuelve una tupla con los datos
        row = self.db.cur.fetchone()

        # Retorna un objeto que representa la conversacion
        return ConversationSQLMapper.from_row(row)
    
    def remplace(self, conversation_id, col, attribute):
        # Obtenemos el sql
        # mas concretamente un UPDATE como este:
        #   UPDATE conversations
        #   SET title = %s
        #   WHERE id = %s
        sql = UpDateConversationsSQL(col=col).build()
        
        # Hace la consulta sql para actualizar la database
        self.db.cur.execute(sql,(attribute, conversation_id))
        

if __name__ == "__main__":
    pass