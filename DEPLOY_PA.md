# Hosting SamiChatbot on PythonAnywhere 🚀👑
**PythonAnywhere**:

### 1. Sube tu código
1. Comprime tu carpeta `SamiChatbot` en un archivo `.zip`.
2. En PythonAnywhere, ve a la pestaña **Files**.
3. Sube el `.zip` y usa la consola (Bash) para descomprimirlo: `unzip SamiChatbot.zip`.

### 2. Configura el Entorno Virtual
En una consola **Bash** de PythonAnywhere, ejecuta:
```bash
mkvirtualenv --python=python3.10 venv
pip install pyTelegramBotAPI python-dotenv requests
```

### 3. Archivo .env
Asegúrate de que tu archivo `.env` esté en la carpeta principal con tus llaves reales:
- `TELEGRAM_BOT_TOKEN`
- `OPENROUTER_API_KEY`

### 4. Ejecutar el Bot
Para que el bot no se detenga al cerrar la consola:

#### Opción A (Cuentas Premium - Recomendado)
Si tienes una cuenta paga, usa la pestaña **Tasks**:
1. Crea una nueva **Always-on task**.
2. Comando: `/home/TU_USUARIO/.virtualenvs/venv/bin/python /home/TU_USUARIO/SamiChatbot/main.py`

#### Opción B (Cuenta Gratuita)
En una cuenta gratis, el proceso se detendrá eventualmente. Para lanzarlo:
1. Abre una consola **Bash**.
2. Ejecuta: `workon venv`
3. Ejecuta: `python main.py`
*Nota: Tendrás que reiniciarlo manualmente si se cae o pasadas 24 horas.*

### ⚠️ Importante (Cuentas Gratis)
PythonAnywhere (Free) tiene una **whitelist** de sitios permitidos. 
- Telegram está permitido.
- **OpenRouter** y la API de clima/moneda podrían estar bloqueados en la versión gratis. Si Andi no responde, revisa el log de errores. Si es así, necesitarás una cuenta paga o usar una API permitida por ellos.