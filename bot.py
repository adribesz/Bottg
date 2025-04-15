import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import signal
import sys

TOKEN = "TU TOKEN"
ADMIN_ID = TU ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋👋 ¡Hola! 👋👋 Envíame tu mensaje y te responderé lo más pronto posible. ☺️☺️')

async def delete_message_later(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Error al eliminar mensaje: {e}")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Mensaje de {user.first_name} (ID: {user.id}):\n\n{update.message.text}"
    )
    confirm_message = await update.message.reply_text("✅ Mensaje recibido. Te responderé pronto 😉")
    
    asyncio.create_task(delete_message_later(confirm_message, 5))

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_ID):
        return
    
    try:
        user_id = context.args[0]
        message = ' '.join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=message)
        await update.message.reply_text("Mensaje enviado.")
    except:
        await update.message.reply_text("Uso: /reply ID_USUARIO mensaje")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", reply))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot detenido manualmente")
    except Exception as e:
        print(f"Error: {e}")
