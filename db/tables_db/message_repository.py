from db.sql_language import InsertSQL, SelectMessagesByConversation
from db.models_db import MessageSQLMapper
from psycopg2 import Error as psycopg2Error
from db.models_db import TableMessenge


# Manejará las principales funciones de la tabla message
class MessageRepository:
    
    # Se le tendrá que pasar una conexion
    # de la base de datos
    def __init__(self, db,):
        self.db = db
 
    # Crea una fila en message
    def save(self, data: TableMessenge):
        # Usa InsertSQL para crea una consulta sql
        # mas concretamente un insert. más o menos como este:
        #     INSERT INTO messages ('id_conversation', "role", "date", "content")
        #     VALUES (%s, %s, %s)
        sql = InsertSQL(
            "messages",
            MessageSQLMapper.COLUMNS
        ).build()

        try:
            # Hace la consulta sql
            # message.to_row() = datos del mensaje
            self.db.cur.execute(sql, MessageSQLMapper.to_row(data))

        except Exception as e:
            self.db.conn.rollback()
            print("Error:", e)

    # Obtener los mensaje de una conversación
    # tenemos que pasarle el id de alguna conversación
    def get_by_conversation(self, conversation_id) -> list[TableMessenge]:
        # Obtenemos el sql
        # mas concretamente un SELECT como este:
        #    SELECT id_conversation, role, date, content
        #    FROM messages
        #    WHERE id_conversation = %s
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