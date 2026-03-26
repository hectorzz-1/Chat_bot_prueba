# Imports librerias externas
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Imports librerias internas
# Agente de IA agent/
from agent.connection import ConnectBrain
from agent.config_IA import JsonSettingsRepository

# Configuraciones Config/
from config.config import BASE_DIR

if __name__ == "__main__":

    # Cargamos claves
    load_dotenv(BASE_DIR / ".env")

    # Nos conectamos con la api
    brain = ConnectBrain(env_key="API_KEY_OPENAI").get_client()

    # Cargar los agentes
    JSON_CONFIG= BASE_DIR / "config" / "agents.json"
    chat_config= JsonSettingsRepository(file=JSON_CONFIG).load()

    