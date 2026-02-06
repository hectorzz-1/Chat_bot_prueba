from db.sql_language import InsertSQL, SelectMessagesByConversation
from db.models_db import MessageSQLMapper


# Manejará las principales funciones de la tabla message
class MessageRepository:
    
    # Se le tendrá que pasar una conexion
    # de la base de datos
    def __init__(self, db):
        self.db = db

    # Crea una fila en message
    def save(self, message: MessageSQLMapper):
        # Usa InsertSQL para crea una consulta sql
        # mas concretamente un insert. más o menos como este:
        #     INSERT INTO messages ('id_conversation', "role", "date", "content")
        #     VALUES (%s, %s, %s)
        sql = InsertSQL(
            "messages",
            message.COLUMNS
        ).build()

        # Hace la consulta sql
        # message.to_row() = datos del mensaje
        self.db.cur.execute(sql, message.to_row())

    # Obtener los mensaje de una conversación
    # tenemos que pasarle el id de alguna conversación
    def get_by_conversation(self, conversation_id):
        # Obtenemos el sql
        # mas concretamente un SELECT como este:
        #    SELECT conversation_id, role, date, content
        #    FROM messages
        #    WHERE conversation_id = %s
        #    ORDER BY date ASC
        sql = SelectMessagesByConversation().SQL

        # Hace la consulta sql
        # conversation_id = el id de alguna conversación
        self.db.cur.execute(sql, (conversation_id,))

        # Devuelve una tupla con los mensajes
        rows = self.db.cur.fetchall()

        # Retorna una lista de objetos
        # donde cada objeto es un mensaje de la conversación
        return [MessageSQLMapper.from_row(row) for row in rows]