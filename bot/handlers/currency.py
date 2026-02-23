from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from bot.conversation.currency_conv import (
    start_currency_conv, get_amount, get_from_curr, get_to_curr, cancel,
    AMOUNT, FROM_CURR, TO_CURR
)

def get_currency_conv_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^💰 Convert Currency$"), start_currency_conv)],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.Regex("^❌ Cancel$"), get_amount)],
            FROM_CURR: [MessageHandler(filters.TEXT & ~filters.Regex("^❌ Cancel$"), get_from_curr)],
            TO_CURR: [MessageHandler(filters.TEXT & ~filters.Regex("^❌ Cancel$"), get_to_curr)],
        },
        fallbacks=[MessageHandler(filters.Regex("^❌ Cancel$"), cancel)],
    )
