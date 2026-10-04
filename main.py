
import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Telegram funcionando!", 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = (
        "Olá! Sou seu bot de análise e simulação.\n\n"
        "Comandos disponíveis:\n"
        "/start - Iniciar\n"
        "/status - Ver situação do bot\n"
        "/id - Mostrar seu ID do Telegram\n"
        "/ajuda - Ver comandos\n\n"
        "Este bot não executa operações na Quotex."
    )
    await update.message.reply_text(mensagem)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot ativo. Aguardando configuração da fonte de dados."
    )

async def meu_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Seu ID do Telegram é: {update.effective_user.id}"
    )

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Iniciar\n"
        "/status - Situação\n"
        "/id - Seu ID\n"
        "/ajuda - Ajuda"
    )

async def iniciar_bot():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("status", status))
    bot.add_handler(CommandHandler("id", meu_id))
    bot.add_handler(CommandHandler("ajuda", ajuda))

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

    await asyncio.Event().wait()

def executar_bot():
    asyncio.run(iniciar_bot())

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Configure TELEGRAM_BOT_TOKEN no Render.")

    threading.Thread(target=executar_bot, daemon=True).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
