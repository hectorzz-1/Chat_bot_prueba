from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

KEYS_USED = {
    "id_chat","temperature","max_tokens","max_input_tokens",
    "presence_penalty","frequency_penalty","model","tokens",
    "name"
    }

models_opcions = {"gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-4-turbo"}