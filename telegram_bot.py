# -*- coding: utf-8 -*-

import os
import telebot
from telebot import types
from dotenv import load_dotenv
from aviasales_api import AviasalesAPI
import threading
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize bot and API
TELEGRAM_BOT_TOKEN='8272052743:AAEQ-cVRTzWv3Jz97hvZcfXCLl-Sd0x4ET8'
AVIASALES_API_TOKEN='da6e66e3b2d3693471857ba592091cec'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
aviasales = AviasalesAPI(AVIASALES_API_TOKEN)

# Store user subscriptions (in production, use a database)
user_subscriptions = {}

logger.info("Bot initialized successfully")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command"""
    welcome_text = """
🛫 **Добро пожаловать в бот поиска авиабилетов!**

Я помогу вам найти самые дешевые авиабилеты из Санкт-Петербурга (LED) в Калининград (KGD).

**Доступные команды:**
/cheapest - Найти самые дешевые билеты
/direct - Найти прямые рейсы
/monthly - Показать тренды цен по месяцам
/subscribe - Подписаться на ежедневные уведомления
/unsubscribe - Отписаться от уведомлений
/help - Показать справку

Давайте найдем для вас лучшие предложения! ✈️
    """
    
    # Create inline keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_cheapest = types.InlineKeyboardButton("💰 Дешевые билеты", callback_data="cheapest")
    btn_direct = types.InlineKeyboardButton("🎯 Прямые рейсы", callback_data="direct")
    btn_monthly = types.InlineKeyboardButton("📊 Тренды цен", callback_data="monthly")
    btn_subscribe = types.InlineKeyboardButton("🔔 Подписаться", callback_data="subscribe")
    btn_website = types.InlineKeyboardButton("🌐 Перейти на сайт", url="https://aviasales.tp.st/veRdGKnb")
    
    markup.add(btn_cheapest, btn_direct)
    markup.add(btn_monthly, btn_subscribe)
    markup.add(btn_website)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def send_help(message):
    """Handle /help command"""
    help_text = """
🆘 **Справка - Доступные команды:**

/start - Запустить бота и показать главное меню
/cheapest - Найти самые дешевые билеты LED → KGD
/direct - Найти только прямые рейсы
/monthly - Показать тренды цен по месяцам
/subscribe - Подписаться на ежедневные уведомления
/unsubscribe - Отписаться от уведомлений
/help - Показать эту справку

**О боте:**
Этот бот ищет авиабилеты из Санкт-Петербурга (LED) в Калининград (KGD) используя данные Aviasales.

**Советы:**
• Используйте кнопки для быстрого доступа
• Подпишитесь на ежедневные обновления о дешевых билетах
• Все цены указаны в российских рублях (RUB)
• Для покупки билетов переходите на официальный сайт Aviasales

Нужна дополнительная помощь? Обратитесь к разработчику! 👨‍💻
    """
    
    # Create inline keyboard with website link
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_cheapest = types.InlineKeyboardButton("💰 Дешевые билеты", callback_data="cheapest")
    btn_website = types.InlineKeyboardButton("🌐 Перейти на сайт", url="https://aviasales.tp.st/veRdGKnb")
    markup.add(btn_cheapest, btn_website)
    
    bot.send_message(message.chat.id, help_text, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['cheapest'])
def get_cheapest_flights(message):
    """Handle /cheapest command"""
    bot.send_message(message.chat.id, "🔍 Ищу самые дешевые билеты... Пожалуйста, подождите.")
    
    try:
        flights = aviasales.get_cheapest_tickets(origin="LED", destination="KGD")
        
        if flights and len(flights) > 0:
            response = "💰 **Самые дешевые билеты LED → KGD:**\n\n"
            
            for i, flight in enumerate(flights[:5], 1):  # Show top 5
                response += f"**{i}.** {aviasales.format_flight_info(flight)}\n"
            
            response += f"\n🕐 Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            response += "\n\n💡 *Для покупки билетов перейдите на сайт Aviasales*"
            
        else:
            response = "❌ Билеты не найдены. Попробуйте позже."
            
    except Exception as e:
        response = f"⚠️ Ошибка при получении данных о рейсах: {str(e)}"
    
    # Add website button to cheapest flights response
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_website = types.InlineKeyboardButton("🌐 Перейти на сайт", url="https://aviasales.tp.st/veRdGKnb")
    btn_direct = types.InlineKeyboardButton("🎯 Прямые рейсы", callback_data="direct")
    markup.add(btn_website, btn_direct)
    
    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['direct'])
def get_direct_flights(message):
    """Handle /direct command"""
    bot.send_message(message.chat.id, "🎯 Ищу прямые рейсы... Пожалуйста, подождите.")
    
    try:
        flights = aviasales.get_direct_flights(origin="LED", destination="KGD")
        
        if flights and len(flights) > 0:
            response = "🎯 **Прямые рейсы LED → KGD:**\n\n"
            
            for i, flight in enumerate(flights[:5], 1):  # Show top 5
                response += f"**{i}.** {aviasales.format_flight_info(flight)}\n"
            
            response += f"\n🕐 Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            response += "\n\n💡 *Для покупки билетов перейдите на сайт Aviasales*"
            
        else:
            response = "❌ Прямые рейсы не найдены. Попробуйте позже."
            
    except Exception as e:
        response = f"⚠️ Ошибка при получении данных о рейсах: {str(e)}"
    
    # Add website button to direct flights response
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_website = types.InlineKeyboardButton("🌐 Перейти на сайт", url="https://aviasales.tp.st/veRdGKnb")
    btn_cheapest = types.InlineKeyboardButton("💰 Дешевые билеты", callback_data="cheapest")
    markup.add(btn_website, btn_cheapest)
    
    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['monthly'])
def get_monthly_trends(message):
    """Handle /monthly command"""
    bot.send_message(message.chat.id, "📊 Получаю тренды цен по месяцам... Пожалуйста, подождите.")
    
    try:
        monthly_data = aviasales.get_monthly_prices(origin="LED", destination="KGD")
        
        if monthly_data and len(monthly_data) > 0:
            response = "📊 **Тренды цен по месяцам LED → KGD:**\n\n"
            
            for data in monthly_data[:6]:  # Show 6 months
                month = data.get('month', 'Н/Д')
                price = data.get('price', 'Н/Д')
                airline = data.get('airline', 'Н/Д')
                
                response += f"📅 **{month}**: {price} руб. ({airline})\n"
            
            response += f"\n🕐 Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            response += "\n\n💡 *Для покупки билетов перейдите на сайт Aviasales*"
            
        else:
            response = "❌ Данные по месяцам недоступны. Попробуйте позже."
            
    except Exception as e:
        response = f"⚠️ Ошибка при получении месячных данных: {str(e)}"
    
    # Add website button to monthly trends response
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_website = types.InlineKeyboardButton("🌐 Перейти на сайт", url="https://aviasales.tp.st/veRdGKnb")
    btn_cheapest = types.InlineKeyboardButton("💰 Дешевые билеты", callback_data="cheapest")
    markup.add(btn_website, btn_cheapest)
    
    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['subscribe'])
def subscribe_user(message):
    """Handle /subscribe command"""
    user_id = message.from_user.id
    
    if user_id not in user_subscriptions:
        user_subscriptions[user_id] = {
            'chat_id': message.chat.id,
            'username': message.from_user.username or message.from_user.first_name,
            'subscribed_at': datetime.now()
        }
        
        response = """
🔔 **Подписка активирована!**

Теперь вы будете получать ежедневные уведомления о самых дешевых билетах из Санкт-Петербурга в Калининград.

**Что вы получите:**
• Ежедневные обновления в 9:00 по московскому времени
• Топ-3 самых дешевых билета
• Уведомления о значительном снижении цен

Используйте /unsubscribe чтобы отписаться в любое время.
        """
    else:
        response = "✅ Вы уже подписаны на ежедневные уведомления о рейсах!"
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe_user(message):
    """Handle /unsubscribe command"""
    user_id = message.from_user.id
    
    if user_id in user_subscriptions:
        del user_subscriptions[user_id]
        response = "❌ **Подписка отменена!**\n\nВы больше не будете получать ежедневные уведомления о рейсах."
    else:
        response = "ℹ️ Вы не подписаны на уведомления."
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Handle inline keyboard callbacks"""
    if call.data == "cheapest":
        get_cheapest_flights(call.message)
    elif call.data == "direct":
        get_direct_flights(call.message)
    elif call.data == "monthly":
        get_monthly_trends(call.message)
    elif call.data == "subscribe":
        subscribe_user(call.message)
    
    # Answer the callback query to remove loading state
    bot.answer_callback_query(call.id)


def send_daily_notifications():
    """Send daily notifications to subscribed users"""
    while True:
        try:
            current_time = datetime.now()
            
            # Send notifications at 9:00 AM (adjust timezone as needed)
            if current_time.hour == 9 and current_time.minute == 0:
                
                if user_subscriptions:
                    print(f"Отправка ежедневных уведомлений {len(user_subscriptions)} пользователям...")
                    
                    # Get cheapest flights
                    flights = aviasales.get_cheapest_tickets(origin="LED", destination="KGD", limit=3)
                    
                    if flights:
                        notification_text = "🌅 **Ежедневная сводка по рейсам - LED → KGD**\n\n"
                        notification_text += "💰 **Топ-3 самых дешевых билета:**\n\n"
                        
                        for i, flight in enumerate(flights, 1):
                            notification_text += f"**{i}.** {aviasales.format_flight_info(flight)}\n"
                        
                        notification_text += f"\n🕐 Обновлено: {current_time.strftime('%Y-%m-%d %H:%M')}"
                        notification_text += "\n\nИспользуйте /unsubscribe чтобы отписаться от уведомлений."
                        
                        # Send to all subscribed users
                        for user_id, user_data in user_subscriptions.copy().items():
                            try:
                                bot.send_message(
                                    user_data['chat_id'], 
                                    notification_text, 
                                    parse_mode='Markdown'
                                )
                            except Exception as e:
                                print(f"Не удалось отправить уведомление пользователю {user_id}: {e}")
                                # Remove user if chat is not accessible
                                if "chat not found" in str(e).lower():
                                    del user_subscriptions[user_id]
                    
                # Wait for 60 seconds to avoid sending multiple times in the same minute
                time.sleep(60)
            
            # Check every 30 seconds
            time.sleep(30)
            
        except Exception as e:
            print(f"Ошибка в ежедневных уведомлениях: {e}")
            time.sleep(60)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Handle all other messages"""
    response = """
🤖 Я не понял эту команду.

Используйте /help чтобы увидеть доступные команды или нажмите кнопки ниже:
    """
    
    # Create inline keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_cheapest = types.InlineKeyboardButton("💰 Дешевые", callback_data="cheapest")
    btn_help = types.InlineKeyboardButton("🆘 Справка", callback_data="help")
    btn_website = types.InlineKeyboardButton("🌐 Перейти на сайт", url="https://aviasales.tp.st/veRdGKnb")
    markup.add(btn_cheapest, btn_help)
    markup.add(btn_website)
    
    bot.send_message(message.chat.id, response, reply_markup=markup)


def main():
    """Main function to start the bot"""
    print("🤖 Запуск бота поиска авиабилетов Aviasales...")
    print(f"Имя бота: @{bot.get_me().username}")
    
    # Start daily notifications in a separate thread
    notification_thread = threading.Thread(target=send_daily_notifications, daemon=True)
    notification_thread.start()
    print("📅 Служба ежедневных уведомлений запущена")
    
    # Start bot polling
    print("🚀 Бот запущен! Нажмите Ctrl+C для остановки.")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка бота: {e}")


if __name__ == "__main__":
    main() 
