import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update

MENU, AI_CHAT, USER_INFO = range(3)
user_data = {}


def btns(tip=None):
    bts = []
    if tip == "menu":
        bts = [
            ["Ijtimoiy tarmoq 🌐", "Chat 💭"]
        ]
    return ReplyKeyboardMarkup(bts, resize_keyboard=True)


def inline_btns(tip=None):
    if tip == "ijtimoiysahifalar":
        bts = [
            [InlineKeyboardButton("Ijtimoiy tarmoqdagi sahifalar 🌐",
                                  callback_data="welkin", url="http://myurls.co/sardorbackend")]
        ]
    return InlineKeyboardMarkup(bts)


keyword_responses = {
    "salom": "Assalomu Alaykum!",
    "hayr": "Xayr. Boshqa savollaringizni yozishingiz mumkin.",
    "nima yangiliklar": "Yangiliklar haqida ma'lumot topshirish uchun Ijtimoiy tarmoq 🌐 tugmasini bosing.",
}


def message_handler(update, context):
    msg = update.message.text
    chat_id = update.message.chat_id

    if msg == "Ijtimoiy tarmoq 🌐":
        context.bot.send_photo(
            chat_id=chat_id,
            photo=open('ijtimoiy.png', 'rb'),
            caption="Ijtimoiy tarmoqdagi barcha sahifalar, kuzatish uchun pasdagi tugmani bosing va kuzatishda davom "
                    "eting!\n\nAgar qandayadir savollar va murojatlar bo'lsa yozib qoldirishingiz mumkin 👇🏻",
            reply_markup=inline_btns("ijtimoiysahifalar"))

    elif msg == "Chat 💭":
        user = update.message.from_user
        update.message.reply_text("Qandaydir savol va murojatlar bo'lsa yozib qoldiring, tez orada sizga "
                                  "Sardor Egamberdiyev'tomonidan jabob yoziladi 👇🏻",
                                  parse_mode="HTML", reply_markup=btns("menu"))


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"Assalomu Alaykum <b>{user.first_name}</b>!\nBotga xush kelibsiz!",
        parse_mode="HTML",
        reply_markup=btns("menu")
    )
    return MENU


def id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    user_info = f"Bu sizning Telegram ma'lumotlaringiz:" \
                f"\n\n[ID: {chat_id}](tg://user?id={chat_id})" \
                f"\nFirst Name: {first_name} \n" \
                f"Last Name: {last_name} " \
                f"\nUser Name: {username}"

    update.message.reply_text(user_info, parse_mode="Markdown", reply_markup=btns("menu"))
    return USER_INFO


def main():
    Token = "5803862247:AAHAgaznBiSO2zGcwQbAvShFpz1TdPVVfgk"
    updater = Updater(Token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("id", id))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
