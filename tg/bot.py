import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
from mirea_db.db import Database
from tg.config import bot_token

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

START_ROUTES, MID_ROUTES, END_ROUTES = range(3)

ONE = 'first'

db = Database(link="localhost:27017")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.chat_id
    logger.info("User %s started the conversation.", user)

    keyboard = [

        [InlineKeyboardButton("ФКБО-01-20", callback_data='1')],
        [InlineKeyboardButton("ФКБО-01-21", callback_data='2')],
        [InlineKeyboardButton("ФКБО-01-22", callback_data='3')],
        [InlineKeyboardButton("ФКБО-01-23", callback_data='4')],
        [InlineKeyboardButton("ФВБО-01-20", callback_data='5')],
        [InlineKeyboardButton("ФВБО-01-21", callback_data='6')],
        [InlineKeyboardButton("ФВБО-01-22", callback_data='7')],
        [InlineKeyboardButton("ФВБО-01-23", callback_data='8')],
        [InlineKeyboardButton("ФЭБО-01-20", callback_data='9')],
        [InlineKeyboardButton("ФЭБО-01-21", callback_data='10')],
        [InlineKeyboardButton("Следующая страница", callback_data='first')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Привет, это бот с расписанием РТУ МИРЭА филиала г. Фрязино. "
                                    "Пожалуйста, выбери свою группу.", reply_markup=reply_markup)

    return START_ROUTES


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("ФЭБО-01-22", callback_data='11')],
        [InlineKeyboardButton("ФЭБО-01-23", callback_data='12')],
        [InlineKeyboardButton("ФКБВ-01-20", callback_data='13')],
        [InlineKeyboardButton("ФКБВ-01-21", callback_data='14')],
        [InlineKeyboardButton("ФКБВ-01-22", callback_data='15')],
        [InlineKeyboardButton("ФКБВ-01-23", callback_data='16')],
        [InlineKeyboardButton("ФРМО-01-22", callback_data='17')],
        [InlineKeyboardButton("ФРМО-01-23", callback_data='18')],
        [InlineKeyboardButton("ФКМО-01-22", callback_data='19')],
        [InlineKeyboardButton("ФКМО-01-23", callback_data='20')],
        [InlineKeyboardButton("Следующая страница", callback_data='second')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Привет, это бот с расписанием РТУ МИРЭА филиала г. Фрязино. "
             "Пожалуйста, выбери свою группу.", reply_markup=reply_markup
    )
    return START_ROUTES


async def tetetete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    # test_values = db.find_lessons_by_group_and_day("ФКБО-01-23", 0, "Понедельник")
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=str('test_values'), reply_markup=reply_markup
    )
    return END_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = update.callback_query.from_user.id
    text = update.callback_query.data
    db.change_user_variable(user_id=user_id, variable_name='user_preference', value=int(text))
    await query.answer()
    await query.edit_message_text(text="Запомнили Ваш выбор. Вы сможете его поменять в любой момент в настройках.")
    return ConversationHandler.END


async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text = update.callback_query.data
    user_id = update.callback_query.from_user.id
    db.fill_user(user_id, int(text))
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("7:00 и 19:00 сегодняшние, 21:00 завтрашние", callback_data='0')],
        [InlineKeyboardButton("Только утром в 7", callback_data='1')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Выбери в какое время тебе присылать уведомления", reply_markup=reply_markup
    )
    return END_ROUTES


def main() -> None:
    application = Application.builder().token(bot_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(new, pattern="^[0-9]+$"),
                CallbackQueryHandler(one, pattern="^first$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(end, pattern="^[0-9]+$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
