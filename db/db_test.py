import psycopg2
import uuid



























if __name__ != "__main__":
    
    # conexión a PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="ai_agent",
        user="agent_user", 
        password="agent_pass",
        port=5432
    )

    cur = conn.cursor()

    # crear conversación
    conversation_id = uuid.uuid4()

    cur.execute(
        "INSERT INTO conversations (id) VALUES (%s)",
        (str(conversation_id),)
    )

    # insertar mensajes
    cur.execute(
        """
        INSERT INTO messages (conversation_id, role, content)
        VALUES (%s, %s, %s)
        """,
        (str(conversation_id), "user", "Hola agente")
    )

    cur.execute(
        """
        INSERT INTO messages (conversation_id, role, content)
        VALUES (%s, %s, %s)
        """,
        (str(conversation_id), "assistant", "Hola humano")
    )

    conn.commit()

    # leer mensajes
    cur.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at
        """,
        (str(conversation_id),)
    )

    rows = cur.fetchall()

    print("\nMensajes guardados:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()