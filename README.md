# 🛫 Aviasales Flight Tracker Telegram Bot

A Telegram bot that helps you find the cheapest flights from Kaliningrad (KGD) to Saint Petersburg (LED) using the Aviasales API.

## ✨ Features

- 💰 **Find Cheapest Flights**: Get the best deals for KGD → LED route
- 🎯 **Direct Flights Only**: Filter for non-stop flights
- 📊 **Monthly Price Trends**: View price trends over months
- 🔔 **Daily Notifications**: Subscribe to daily flight updates
- 🤖 **Interactive Interface**: Easy-to-use inline keyboards
- 🌍 **Real-time Data**: Live flight data from Aviasales

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Aviasales API Token (from [Travelpayouts](https://www.travelpayouts.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TG_Aviasales
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Copy the example environment file:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file and add your tokens:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   AVIASALES_API_TOKEN=your_aviasales_api_token_here
   ```

4. **Run the bot**
   ```bash
   python telegram_bot.py
   ```

## 🔧 Configuration

### Getting Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the provided token to your `.env` file

### Getting Aviasales API Token

1. Visit [Travelpayouts](https://www.travelpayouts.com/)
2. Sign up for a free account
3. Go to API section and get your token
4. Add the token to your `.env` file

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see main menu |
| `/cheapest` | Get current cheapest flights KGD → LED |
| `/direct` | Get direct flights only |
| `/monthly` | Get monthly price trends |
| `/subscribe` | Subscribe to daily flight notifications |
| `/unsubscribe` | Stop daily notifications |
| `/help` | Show help message |

## 🏗️ Project Structure

```
TG_Aviasales/
├── telegram_bot.py      # Main bot file
├── aviasales_api.py     # Aviasales API wrapper
├── requirements.txt     # Python dependencies
├── env_example.txt      # Environment variables example
├── .env                 # Your environment variables (create this)
└── README.md           # This file
```

## 🔄 How It Works

1. **User Interaction**: Users interact with the bot through commands or inline buttons
2. **API Requests**: Bot makes requests to Aviasales API for flight data
3. **Data Processing**: Flight information is formatted and presented to users
4. **Notifications**: Subscribed users receive daily updates at 9:00 AM

## 📊 API Endpoints Used

- **Cheapest Tickets**: `/v1/prices/cheap` - Get cheapest available flights
- **Direct Flights**: `/v1/prices/direct` - Get non-stop flights only
- **Monthly Prices**: `/v1/prices/monthly` - Get monthly price trends

## 🛠️ Development

### File Descriptions

- **`telegram_bot.py`**: Main bot logic, command handlers, and user interface
- **`aviasales_api.py`**: API wrapper class for Aviasales integration
- **`requirements.txt`**: Python package dependencies
- **`env_example.txt`**: Template for environment variables

### Adding New Features

1. **New Commands**: Add message handlers in `telegram_bot.py`
2. **API Methods**: Extend `AviasalesAPI` class in `aviasales_api.py`
3. **Notifications**: Modify `send_daily_notifications()` function

## 🔔 Daily Notifications

Users can subscribe to receive daily flight updates:

- **Time**: 9:00 AM (configurable)
- **Content**: Top 3 cheapest flights
- **Frequency**: Once per day
- **Management**: Users can subscribe/unsubscribe anytime

## ⚠️ Important Notes

- **Rate Limits**: Aviasales API has rate limits - avoid excessive requests
- **Data Accuracy**: Flight prices and availability change frequently
- **Timezone**: Notification time is based on server timezone
- **Storage**: User subscriptions are stored in memory (use database for production)

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if tokens are correctly set in `.env` file
   - Verify internet connection
   - Check console for error messages

2. **No flight data**
   - Verify Aviasales API token is valid
   - Check if API endpoints are accessible
   - Route KGD → LED might have limited flights

3. **Notifications not working**
   - Check server timezone settings
   - Verify notification thread is running
   - Check console logs for errors

### Error Messages

- `TELEGRAM_BOT_TOKEN not found`: Add your bot token to `.env` file
- `AVIASALES_API_TOKEN not found`: Add your API token to `.env` file
- `API request error`: Check internet connection and API token validity

## 📈 Future Enhancements

- 🗄️ **Database Integration**: Store user data persistently
- 🌍 **Multiple Routes**: Support for different flight routes
- 💱 **Currency Options**: Support for different currencies
- 📅 **Date Selection**: Allow users to specify travel dates
- 🔍 **Price Alerts**: Notify when prices drop below threshold
- 📱 **Web Interface**: Add web dashboard for management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Review the console logs
3. Verify your API tokens
4. Check Aviasales API documentation

## 🙏 Acknowledgments

- [Aviasales](https://aviasales.ru/) for flight data API
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) for Telegram integration
- [Travelpayouts](https://www.travelpayouts.com/) for API access

---

**Happy Flying! ✈️** 