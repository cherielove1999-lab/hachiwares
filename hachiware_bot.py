import telebot
import random
import os  # <--- Добавляем эту библиотеку

# Бот будет брать токен из настроек Railway, а не из кода
TOKEN = os.environ.get("TELEGRAM_TOKEN") 
bot = telebot.TeleBot(TOKEN)

# ... дальше идет ВЕСЬ ВАШ ОСТАЛЬНОЙ КОД (фразы, обработчики и т.д.) ...

# 1. Сначала объявляем переменную с эмодзи
premium_emoji_tag = '<tg-emoji emoji-id="5242553367737154940">🐱</tg-emoji>'
premium_emoji_tag1 = '<tg-emoji emoji-id="5244717666182116618">😽</tg-emoji>'
premium_emoji_tag2 = '<tg-emoji emoji-id="6039328191225534740">😊</tg-emoji>'

# 2. ВАЖНО: добавляем букву f перед строками, где используется {premium_emoji_tag}
pill_phrases = [
    f"Мяу! {premium_emoji_tag} Вот тебе сладкая пилюля от Хачивары! 🍬💊 Пусть все печали растворятся!",
    f"Хачивара прописывает: одну сладкую пилюлю счастья! Принимать с улыбкой! {premium_emoji_tag}💊",
    "Сладкая пилюля доставлена! 🍭 Хачивара говорит: ты справишься, ты классная! 🐾",
    f"Доктор Хачивара выписал тебе сладкую пилюлю 🍫. Побочный эффект: мурчание и отличное настроение! {premium_emoji_tag1}",
]

smile_phrases = [
    f"Улыбка доктора Хачивары активирована! {premium_emoji_tag2}🩺 Срочно улыбнись в ответ, мяу! {premium_emoji_tag}",
    f"Доктор Хачивара говорит: улыбка — лучшее лекарство! Вот тебе немного волшебства: ✨{premium_emoji_tag1}",
    f"Хачивара сделал улыбку доктора! Теперь ты официально не можешь грустить! {premium_emoji_tag}🐾",
    f"Улыбка доктора Хачивары: +100 к настроению! {premium_emoji_tag2}🐈‍⬛ Попробуй не улыбнуться в ответ — не получится!",
]

# Приветствие по команде /start (добавлен parse_mode='HTML' и f-строка)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        f"Привет! Я Хачивара, твой личный доктор хорошего настроения! {premium_emoji_tag}💖\n"
        "Напиши мне «сладкая пилюля» или «улыбка доктора», и я подниму тебе настроение!\n"
        "Также можно использовать команды /pill и /smile.",
        parse_mode='HTML'
    )

# Обработка текстовой фразы «сладкая пилюля» (ОСТАВЛЕН ТОЛЬКО ОДИН ОБРАБОТЧИК)
@bot.message_handler(func=lambda message: message.text and 'сладкая пилюля' in message.text.lower())
def handle_sweet_pill(message):
    bot.reply_to(message, random.choice(pill_phrases), parse_mode='HTML')

# Обработка текстовой фразы «улыбка доктора»
@bot.message_handler(func=lambda message: message.text and 'улыбка доктора' in message.text.lower())
def handle_doctor_smile(message):
    bot.reply_to(message, random.choice(smile_phrases), parse_mode='HTML')

# Дублирующие слэш-команды для удобства
@bot.message_handler(commands=['pill'])
def cmd_pill(message):
    bot.reply_to(message, random.choice(pill_phrases), parse_mode='HTML')

@bot.message_handler(commands=['smile'])
def cmd_smile(message):
    bot.reply_to(message, random.choice(smile_phrases), parse_mode='HTML')

# --- НАЧАЛО КОДА ДЛЯ ИНЛАЙН-РЕЖИМА ---

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query_text(query):
    query_text = query.query.lower()
    
    if 'сладкая пилюля' in query_text:
        result_text = random.choice(pill_phrases)
        title = "Сладкая пилюля от Хачивары 💊"
    elif 'улыбка доктора' in query_text:
        result_text = random.choice(smile_phrases)
        title = f"Улыбка доктора Хачивары {premium_emoji_tag2}"
    else:
        result_text = f"Хачивара не знает такой команды, мяу! {premium_emoji_tag} Попробуй написать «сладкая пилюля» или «улыбка доктора»."
        title = "Подсказка от Хачивары 🐾"

    result = telebot.types.InlineQueryResultArticle(
        id='1',
        title=title,
        description=result_text,
        input_message_content=telebot.types.InputTextMessageContent(
            message_text=result_text,
            parse_mode='HTML' # Обязательно для инлайн-режима
        )
    )
    
    bot.answer_inline_query(query.id, [result])

# --- КОНЕЦ КОДА ДЛЯ ИНЛАЙН-РЕЖИМА ---

# Запуск бота
if __name__ == '__main__':
    # В консоль лучше выводить обычный эмодзи, так как HTML-теги там не работают
    print("Хачивара на посту! 🐱💊") 
    bot.infinity_polling()
