from db.sql_language import (
    SelectAgentSQL, InsertSQL, UpDateAgentSQL,
    SelectAgentByIdSQL, SelectByNameSQL
    )
from db.models_db import TableAgent, AgentSQLMapper


class AgentRepository:

    def __init__(self, db):
        self.db = db

    # Cargamos todos los agentes
    def get_all(self) -> list[TableAgent]:
        # Obtenemos el sql
        sql = SelectAgentSQL().SQL

        # Hace la consulta sql
        self.db.cur.execute(sql)
        # Devuelve una tupla con los agentes
        rows = self.db.cur.fetchall()

        #retornamos una lista con los agentes
        return [AgentSQLMapper.from_row(row) for row in rows]
    
    # Creamos un agente nuevo
    def create(self, data : TableAgent) -> None:
        # Obtenemos el sql
        sql = InsertSQL(
            table= "agent",
            columns= AgentSQLMapper.COLUMNS,
        ).build()

        try:
            # Hace la consulta sql
            self.db.cur.execute(sql, AgentSQLMapper.to_row(data))
            # guardamos
            self.db.conn.commit()
        
        except Exception as e:
            self.db.conn.rollback()
            print("Error:", e)

    # Actualizamos un dato
    def remplace(self, agent_id, column, attribute) -> None:
        # Obtenemos el sql
        sql = UpDateAgentSQL(
            column= column
        ).build()

        try: 
            # Hace la consulta sql para actualizar la database
            self.db.cur.execute(sql,(attribute, agent_id))
        except Exception as e:
            self.db.conn.rollback()
            print("Error:", e)

    def get_by_id(self, agent_id) -> TableAgent:
        # Obtenemos el sql
        sql = SelectAgentByIdSQL.SQL

        # Hace la consulta sql
        self.db.cur.execute(sql, (str(agent_id),))
        # Devuelve una tupla con los datos
        row = self.db.cur.fetchone()

        # Retorna el agente abstraido en un objeto
        return AgentSQLMapper.from_row(row)

    def get_by_name(self, agent_name) -> TableAgent:
        # Obtenemos el sql
        sql = SelectByNameSQL.SQL

        # Hacemos la query sql
        # Hace la consulta sql
        self.db.cur.execute(sql, (agent_name,))
        # Devuelve una tupla con los datos
        row = self.db.cur.fetchone()

        # Retorna el agente abstraido en un objeto
        return AgentSQLMapper.from_row(row)
        