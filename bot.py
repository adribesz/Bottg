import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Obtener variables de entorno
TOKEN = os.environ.get('TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))  # Convertir a entero

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# El resto de tu código se mantiene igual...

def main():
    # Verificar que las variables de entorno existen
    if not TOKEN or not ADMIN_ID:
        logger.error("Token o ADMIN_ID no configurados en variables de entorno")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", reply))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot detenido manualmente")
    except Exception as e:
        print(f"Error: {e}")
