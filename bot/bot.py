import telebot
from telebot import types
import sqlite3
from datetime import datetime

# ===== ТВОИ ДАННЫЕ =====
TOKEN = '8263285109:AAF8SQ49qvmFaZWayJ-PhuHzhiwf8n_lK-Q'
ADMIN_ID = '8530087502'
bot = telebot.TeleBot(TOKEN)

# ===== БАЗА ДАННЫХ =====
conn = sqlite3.connect('orders.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id TEXT,
 username TEXT,
 first_name TEXT,
 product_name TEXT,
 price TEXT,
 size TEXT,
 material TEXT,
 delivery_type TEXT,
 address TEXT,
 phone TEXT,
 status TEXT,
 created_at TEXT
)
''')
conn.commit()

# ===== ХРАНИЛИЩЕ ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ =====
user_data = {}

# ===== ПРОСТЕЙШИЙ ОБРАБОТЧИК START =====
@bot.message_handler(commands=['start'])
def start(message):
    print(f"👤 Пользователь @{message.from_user.username} запустил бота")
    print(f"📝 Текст команды: {message.text}")
    
    # Разбираем параметры из ссылки
    args = message.text.split()
    
    if len(args) > 1 and args[1].startswith('product_'):
        try:
            # Декодируем параметры
            params = args[1].replace('product_', '').split('_')
            
            if len(params) >= 2:
                product_name = params[0].replace('%20', ' ')
                price = params[1]
                
                print(f"✅ Выбрал товар: {product_name}, цена: {price}")
                
                # Сохраняем данные
                user_data[message.chat.id] = {
                    'product_name': product_name,
                    'price': price,
                    'step': 'waiting_size'
                }
                
                # Создаем клавиатуру
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('📏 180 см', '📏 200 см', '📏 220 см')
                
                # Отправляем сообщение
                bot.send_message(
                    message.chat.id,
                    f"✅ *ВЫ ВЫБРАЛИ:*\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"📦 *Товар:* {product_name}\n"
                    f"💰 *Цена:* {price} ₽\n"
                    f"━━━━━━━━━━━━━━━━━━\n\n"
                    f"📏 *Выберите размер:*",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
                return
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    # Если пришли без параметров или ошибка
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🛒 Каталог на сайте', '📞 Связаться с менеджером')
    
    bot.send_message(
        message.chat.id,
        "👋 *Добро пожаловать!*\n\nВыберите действие:",
        parse_mode='Markdown',
        reply_markup=markup
    )

# ===== ОБРАБОТКА РАЗМЕРА =====
@bot.message_handler(func=lambda message: message.text and '📏' in message.text)
def handle_size(message):
    print(f"📏 Выбрал размер: {message.text}")
    chat_id = message.chat.id
    
    if chat_id in user_data:
        user_data[chat_id]['size'] = message.text.replace('📏 ', '')
        user_data[chat_id]['step'] = 'waiting_material'
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🪵 Дуб', '🪵 Сосна', '🪵 Металл')
        
        bot.send_message(
            chat_id,
            "🪵 *Выберите материал:*",
            parse_mode='Markdown',
            reply_markup=markup
        )

# ===== ОБРАБОТКА МАТЕРИАЛА =====
@bot.message_handler(func=lambda message: message.text and '🪵' in message.text)
def handle_material(message):
    print(f"🪵 Выбрал материал: {message.text}")
    chat_id = message.chat.id
    
    if chat_id in user_data:
        user_data[chat_id]['material'] = message.text.replace('🪵 ', '')
        user_data[chat_id]['step'] = 'waiting_delivery'
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🚚 Доставка', '🚶 Самовывоз')
        
        bot.send_message(
            chat_id,
            "🚚 *Выберите способ получения:*",
            parse_mode='Markdown',
            reply_markup=markup
        )

# ===== ОБРАБОТКА ДОСТАВКИ =====
@bot.message_handler(func=lambda message: message.text in ['🚚 Доставка', '🚶 Самовывоз'])
def handle_delivery(message):
    print(f"🚚 Выбрал доставку: {message.text}")
    chat_id = message.chat.id
    
    if chat_id in user_data:
        user_data[chat_id]['delivery_type'] = message.text
        user_data[chat_id]['step'] = 'waiting_phone'
        
        bot.send_message(
            chat_id,
            "📞 *Введите номер телефона:*",
            parse_mode='Markdown',
            reply_markup=types.ReplyKeyboardRemove()
        )

# ===== ОБРАБОТКА ТЕЛЕФОНА =====
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    
    if chat_id in user_data:
        step = user_data[chat_id].get('step')
        
        if step == 'waiting_phone':
            user_data[chat_id]['phone'] = message.text
            
            if user_data[chat_id]['delivery_type'] == '🚚 Доставка':
                user_data[chat_id]['step'] = 'waiting_address'
                bot.send_message(
                    chat_id,
                    "📍 *Введите адрес доставки:*",
                    parse_mode='Markdown'
                )
            else:
                show_confirmation(chat_id)
        
        elif step == 'waiting_address':
            user_data[chat_id]['address'] = message.text
            show_confirmation(chat_id)

def show_confirmation(chat_id):
    data = user_data[chat_id]
    
    text = (
        f"📋 *ПРОВЕРЬТЕ ДАННЫЕ:*\n\n"
        f"📦 Товар: {data['product_name']}\n"
        f"💰 Цена: {data['price']} ₽\n"
        f"📏 Размер: {data['size']}\n"
        f"🪵 Материал: {data['material']}\n"
        f"🚚 Доставка: {data['delivery_type']}\n"
    )
    
    if 'address' in data:
        text += f"📍 Адрес: {data['address']}\n"
    
    text += f"📞 Телефон: {data['phone']}\n\n"
    text += "✅ *Подтверждаете?*"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Да", callback_data="confirm"),
        types.InlineKeyboardButton("❌ Нет", callback_data="cancel")
    )
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)

# ===== ПОДТВЕРЖДЕНИЕ =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    
    if call.data == "confirm":
        data = user_data[chat_id]
        
        # Отправляем админу
        admin_text = (
            f"🔥 *НОВЫЙ ЗАКАЗ!*\n\n"
            f"👤 @{call.from_user.username}\n"
            f"📦 {data['product_name']}\n"
            f"💰 {data['price']} ₽\n"
            f"📏 {data['size']}\n"
            f"🪵 {data['material']}\n"
            f"🚚 {data['delivery_type']}\n"
        )
        if 'address' in data:
            admin_text += f"📍 {data['address']}\n"
        admin_text += f"📞 {data['phone']}"
        
        bot.send_message(ADMIN_ID, admin_text, parse_mode='Markdown')
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="✅ *ЗАКАЗ ПРИНЯТ!*\n\nМенеджер свяжется с вами.",
            parse_mode='Markdown'
        )
        
        del user_data[chat_id]
    
    elif call.data == "cancel":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="❌ Заказ отменен",
            parse_mode='Markdown'
        )
        if chat_id in user_data:
            del user_data[chat_id]

# ===== ЗАПУСК =====
if __name__ == '__main__':
    print("🚀 Бот запускается...")
    print(f"🔑 Токен: {TOKEN[:10]}...")
    print(f"👤 Admin ID: {ADMIN_ID}")
    print("📦 Ожидаем заказы...")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка: {e}")