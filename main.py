from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# SOZLAMALAR
# =========================

TOKEN = "8743221106:AAFbFmTlRZIYcEK60UV9ORILQCE16JPYyZs"

# Kanal username (masalan: @kanalim)
CHANNEL_USERNAME = "https://t.me/xdkxt"

# Ovoz berish variantlari
candidates = {
    "1": {"name": "1-Bekchanova Anagul Madirimovna", "votes": 0},
    "2": {"name": "2-Ibadullaeva Salamat Jumabaevna", "votes": 0},
    "3": {"name": "3-Yaqubov Baxtiyor Yusupovich", "votes": 0},
    "4": {"name": "4-Vaisov Feruz Axmedjonovich", "votes": 0},
    "5": {"name": "5-Odambaeva Aqida Beknazar qizi", "votes": 0},
    "6": {"name": "6-Xudayberganova Saboxat Shavkat qizi", "votes": 0},
    "7": {"name": "7-Sultonova Nodira Rajjaboevna", "votes": 0},
    "8": {"name": "8-Abdullaev Kaxramon Maxmudovich", "votes": 0},
    "9": {"name": "9-Yusupov Kamoladdin Azadovich", "votes": 0},
    "10": {"name": "10-Sharipova Nazokat Rustambaevna", "votes": 0},
    "11": {"name": "11-Xudaybergenov Farxod Adamovich", "votes": 0},
    "12": {"name": "12-Abdullaev  Ergashboy  Bobojonovich", "votes": 0},
    "13": {"name": "13-Satimova Sayyora", "votes": 0},
    "14": {"name": "14-Raxmanov Satimbay Otajonovich", "votes": 0},
    "15": {"name": "15-Rajabov Otabek Rustambekovich", "votes": 0},
    "16": {"name": "16-Qurambaev Otajon Xasanboevich", "votes": 0},
    "17": {"name": "17-Ismailova Zulfiya", "votes": 0},
    "18": {"name": "18-Ibadullaev Baxodir Ataxonovich", "votes": 0},
    "19": {"name": "19-Matqurbonov Ne’mat Karimboevich", "votes": 0},
    "20": {"name": "20-Davlatov Ulug‘bek Jumaniyozovich", "votes": 0},
    "21": {"name": "21-Qurbonboev Qudrat Jumanazarovich", "votes": 0},
    "22": {"name": "22-Qurbanova Raxat Allaberganovna", "votes": 0},
    "23": {"name": "23-Abdiramanov Xajibay Ruziyevich", "votes": 0},
    "24": {"name": "24-Abdullaev Timur Shoxnazarovich", "votes": 0},
    "25": {"name": "25-Sobirov Egamberdi Sultonovich", "votes": 0},
}

# Kim ovoz berganini saqlash
voted_users = set()


# =========================
# KANALGA OBUNANI TEKSHIRISH
# =========================

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member("@xdkxt", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# =========================
# /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    subscribed = await check_subscription(user_id, context)

    if not subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Ovoz berish uchun avval kanalga obuna bo‘ling.",
            reply_markup=reply_markup
        )
        return

    await show_voting_menu(update, context)


# =========================
# OVOZ BERISH MENYUSI
# =========================

async def show_voting_menu(update, context):
    keyboard = []

    for key, value in candidates.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{value['name']} ({value['votes']} ovoz)",
                callback_data=f"vote_{key}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "🗳 Deputatga ovoz bering:"

    if update.callback_query:
        await update.callback_query.message.reply_text(
            text,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=reply_markup
        )


# =========================
# BUTTONLAR
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    # Obunani tekshirish
    if query.data == "check_sub":
        subscribed = await check_subscription(user_id, context)

        if not subscribed:
            await query.message.reply_text(
                "Siz hali kanalga obuna bo‘lmagansiz."
            )
            return

        await query.message.reply_text(
            "Obuna tasdiqlandi ✅"
        )

        await show_voting_menu(update, context)
        return

    # Ovoz berish
    if query.data.startswith("vote_"):
        if user_id in voted_users:
            await query.message.reply_text(
                "Siz allaqachon ovoz bergansiz ❗"
            )
            return

        candidate_id = query.data.split("_")[1]

        if candidate_id in candidates:
            candidates[candidate_id]["votes"] += 1
            voted_users.add(user_id)

            await query.message.reply_text(
                f"✅ Siz {candidates[candidate_id]['name']} ga ovoz berdingiz!"
            )


# =========================
# ADMIN STATISTIKA
# =========================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📊 Ovozlar statistikasi:\n\n"

    for value in candidates.values():
        text += f"{value['name']} — {value['votes']} ovoz\n"

    await update.message.reply_text(text)


# =========================
# BOTNI ISHGA TUSHIRISH
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
