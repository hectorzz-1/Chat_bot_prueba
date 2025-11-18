# 🤖 Sistema de Agentes IA Personalizados (CLI)

Este proyecto implementa un **sistema de agentes IA configurables** capaces de mantener memoria, realizar consultas a modelos OpenAI y conservar historiales de conversación.  
Todo se ejecuta desde una **interfaz de línea de comandos (CLI)** y utiliza un conjunto modular de clases para validación, configuración, conexión y almacenamiento.

---

## 🚀 Características principales

### ✔ Crear agentes IA personalizados

Puedes crear múltiples agentes, cada uno con:

- Nombre
- Comportamiento base (behavior)
- Modelo de IA a usar
- Instrucciones globales inmutables

Los agentes se guardan en `config.json` y pueden reutilizarse en futuras sesiones.

---

### ✔ Memoria persistente

Cada agente mantiene:

- Tokens usados
- Historial de mensajes (`memory`)
- Comportamiento predefinido
- Restricciones e instrucciones obligatorias

---

### ✔ Historial estructurado de conversaciones

Las conversaciones se guardan en `history.json` como una lista de sesiones:

```json
[
  {
    "date": "2025-11-13 12:45",
    "parley": [
      { "role": "user", "content": "..." },
      { "role": "assistant", "content": "..." }
    ]
  }
]
```

El sistema:

Corrige automáticamente archivos dañados.

Convierte dict → lista si el usuario borró accidentalmente el formato.

Actualiza el último chat o añade uno nuevo.

✔ Validación robusta
Antes de procesar cualquier solicitud, se valida:

Si el texto está vacío

Si contiene espacios inválidos

Si respeta el límite de tokens

Si el modelo seleccionado es válido

✔ Conexión modular con OpenAI
Módulo connection.ConnectBrain:

Crea el cliente OpenAI usando la clave API en .env

Permite cambiar fácilmente el backend en el futuro

✔ Instrucciones automáticas
Todo agente recibe una instrucción fija inicial:

“Nunca digas una grosería o algo despectivo a alguna persona…”

Esto garantiza que el agente mantenga siempre la regla, aunque el usuario intente modificar su comportamiento.

📁 Estructura del proyecto
pgsql
Copiar código

```json
├── main.py
├── config.json
├── history.json
├── connection.py
├── config_IA.py
├── initialize.py
├── actions.py
├── valid.py
├── valid_queries.py
├── text_validators.py
├── make_queries.py
├── parley_control.py
└── .env
```

⚙️ Flujo de ejecución del programa
1️⃣ Inicialización
El archivo main.py:

Cargue la API Key desde un .env

Carga o crea config.json mediante JsonInitConfig

Registra los módulos de configuración y validación

2️⃣ Selección de un agente
Al iniciar:

Si no hay agentes → se crea uno nuevo

Si existen → se muestran y el usuario elige uno

También puede elegir crear uno nuevo

Cada agente recibe la instrucción fija configurada.

3️⃣ Inicio de conversación
El programa:

Muestra un saludo inicial

Crea un registro de sesión con:

Fecha

Lista vacía de mensajes (parley)

4️⃣ Ciclo de conversación
Cada vuelta del loop hace:

Recibir input del usuario

Validar texto

Contar tokens

Verificar límites

Enviar la consulta a OpenAI

Recibir y procesar la respuesta

Guardar ambos mensajes en agent["memory"]

Registrar la conversación en history.json

5️⃣ Manejo del historial
El historial está diseñado para ser siempre una lista de sesiones.

El sistema:

Detecta si el archivo existe

Lo convierte en lista si está mal formado

Si la conversación es nueva → se añade

Si ya está en curso → actualiza el último elemento

6️⃣ Límite de tokens
Si el usuario supera los límites:

Se termina la conversación

El agente restablece su memoria a la instrucción inicial (ParleyForget)

🔧 Requisitos
Python 3.10+

OpenAI Python SDK

dotenv (python-dotenv)

Instalar dependencias:

bash
Copiar código
pip install openai python-dotenv
🔑 Configurar la API Key
En un archivo .env:

ini
Copiar código
API_KEY_OPENAI=tu_api_key_aquí
▶️ Ejecución
bash
Copiar código
python main.py
📄 Licencia
Este proyecto es de uso personal del desarrollador.
Si deseas reutilizar partes del framework, asegúrate de revisar las dependencias y módulos personalizados.

🧩 Notas finales
Este proyecto está construido con una arquitectura modular que permite:

Sustituir modelos fácilmente

Cambiar validadores

Añadir nuevos tipos de acciones (guardar en DB, exportar PDF, etc.)

Integrarlo en interfaces gráficas en el futuro
