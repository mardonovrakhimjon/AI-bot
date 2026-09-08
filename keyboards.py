from telegram import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboard():
    buttons = [
        [KeyboardButton("Mavzular")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


async def get_topics_keyboard():
    buttons = [
        [KeyboardButton("😺 Mushuk rasm"), KeyboardButton("🐶 Kuchuk rasm")],
        [KeyboardButton("🎲 Tasodifiy Raqam"), KeyboardButton("💳 Plastik Karta")],
        [KeyboardButton("⬅️ Orqaga")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
