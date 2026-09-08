import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import keyboards
import services
from settings import Settings


async def save_user(user_id, full_name, username):
    file_name = "users.json"
    
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            users = json.load(file)
    else:
        users = {}
        
    if str(user_id) not in users:
        users[str(user_id)] = {"full_name": full_name, "username": username}
        
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    await save_user(
        user_id=user.id, full_name=user.full_name, username=user.username
    )
    
    await update.message.reply_text(
        f"Salom, {user.full_name}! Botga xush kelibsiz.\n"
        f"Mavzularni ko'rish uchun quyidagi tugmani bosing:",
        reply_markup=await keyboards.get_main_keyboard(),
    )
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Agar foydalanuvchi matn yuborgan bo'lsa
    if update.message.text:
        text = update.message.text.strip()
        
        # Avvalgi tugmalar shartini saqlab qolamiz:
        if "Mavzular" in text:
            await update.message.reply_text(
                "🗂 Kerakli bo'limni tanlang:",
                reply_markup=await keyboards.get_topics_keyboard()
            )
            return
        elif "😺 Mushuk rasm" in text:
            await update.message.reply_text("😺 Mushuk rasmi yuklanmoqda... ")
            img_url = await services.get_cat_image()
            if img_url:
                await update.message.reply_photo(photo=img_url)
            else:
                await update.message.reply_text("Rasm yuklashda xatolik yuz berdi.")
            return
        elif "🐶 Kuchuk rasm" in text:
            await update.message.reply_text("🐶 Kuchuk rasmi yuklanmoqda... ")
            img_url = await services.get_dog_image()
            if img_url:
                await update.message.reply_photo(photo=img_url)
            else:
                await update.message.reply_text("Rasm yuklashda xatolik yuz berdi.")
            return
        elif "🎲 Tasodifiy Raqam" in text:
            num = await services.get_random_number()
            await update.message.reply_text(f"🎲 Tasodifiy raqam: **{num}**", parse_mode="Markdown")
            return
        elif "💳 Plastik Karta" in text:
            card_details = await services.get_random_card()
            await update.message.reply_text(card_details, parse_mode="Markdown")
            return
        elif "⬅️ Orqaga" in text or "⬅️" in text:
            await update.message.reply_text(
                "⬅️ Bosh menyuga qaytdingiz.",
                reply_markup=await keyboards.get_main_keyboard()
            )
            return
        else:
            # Oddiy matn bo'lsa, o'zini qaytaradi
            await update.message.reply_text(text)
            return

    # RASM TASHALSA (Rasm tagida matni bo'lsa uni ham qo'shib qaytaradi)
    elif update.message.photo:
        await update.message.reply_photo(
            photo=update.message.photo[-1].file_id, 
            caption=update.message.caption
        )
        return

    # VIDEO TASHALSA
    elif update.message.video:
        await update.message.reply_video(
            video=update.message.video.file_id, 
            caption=update.message.caption
        )
        return

    # DUMALOQ VIDEO (Video Note) TASHALSA
    elif update.message.video_note:
        await update.message.reply_video_note(
            video_note=update.message.video_note.file_id
        )
        return

    # OVOZLI XABAR (Voice) TASHALSA
    elif update.message.voice:
        await update.message.reply_voice(
            voice=update.message.voice.file_id
        )
        return

    # MUSIQA/QO'SHIQ (Audio) TASHALSA
    elif update.message.audio:
        await update.message.reply_audio(
            audio=update.message.audio.file_id, 
            caption=update.message.caption
        )
        return

    # HUJJAT/FAYL (Document) TASHALSA
    elif update.message.document:
        await update.message.reply_document(
            document=update.message.document.file_id, 
            caption=update.message.caption
        )
        return

    # STIKER TASHALSA
    elif update.message.sticker:
        await update.message.reply_sticker(
            sticker=update.message.sticker.file_id
        )
        return


def main():
    # Yangi v20+ strukturasi bo'yicha botni yaratish
    application = Application.builder().token(Settings.TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Yangi bot faol...")
    
    # Botni polling rejimida ishga tushirish
    application.run_polling()


if __name__ == '__main__':
    main()
