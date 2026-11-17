import telebot
import random
import os
from openai import OpenAI

# --- Инициализация бота ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- Настройка клиента для OpenRouter ---
# Ключ берём из переменной окружения (добавим его на Railway позже)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Проверка, чтобы избежать ошибки 401 Unauthorized
if not OPENROUTER_API_KEY:
    raise ValueError("Не найден ключ OPENROUTER_API_KEY. Проверьте переменные на Railway.")

# Создаём клиент, указывая адрес API OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

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

@bot.message_handler(func=lambda message: message.text and 'сладкая пилюля' in message.text.lower())
def handle_sweet_pill(message):
    bot.reply_to(message, random.choice(pill_phrases), parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text and 'улыбка доктора' in message.text.lower())
def handle_doctor_smile(message):
    bot.reply_to(message, random.choice(smile_phrases), parse_mode='HTML')

@bot.message_handler(commands=['pill'])
def cmd_pill(message):
    bot.reply_to(message, random.choice(pill_phrases), parse_mode='HTML')

@bot.message_handler(commands=['smile'])
def cmd_smile(message):
    bot.reply_to(message, random.choice(smile_phrases), parse_mode='HTML')

# --- ИИ ОБРАБОТЧИК (СЮДА ВСТАВЛЕН ТОТ САМЫЙ КУСОК КОДА) ---
# Этот обработчик ловит ВСЕ остальные текстовые сообщения
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_ai_message(message):
    # Показываем статус "печатает..."
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # ВОТ ОН, ЗАПРОС К OPENROUTER:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",  # Бесплатная модель
            messages=[
                {"role": "system", "content": "Ты — Хачивара, милый и заботливый котик-доктор. Отвечай с любовью, эмодзи и заботой. Твоя цель — поднять настроение."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=500
        )
        
        # Отправляем ответ от нейросети
        bot.reply_to(message, response.choices[0].message.content)
        
    except Exception as e:
        # Если произошла ошибка (например, закончились лимиты), пишем в консоль и пользователю
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(message, "Мяу... Мои кошачьи мозги перегрелись, пока я думал над ответом. 🐾 Попробуй еще раз чуть позже!")

# --- ЗАПУСК ---
if __name__ == '__main__':
    print(f"Хачивара на посту! {premium_emoji_tag}💊")
    # Добавляем threaded=True, чтобы бот не зависал на одном запросе
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
