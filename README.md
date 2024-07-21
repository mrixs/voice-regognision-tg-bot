# Telegram Voice to Text Bot
This is a Python script that creates a Telegram bot which can recognize the voice message and convert it into text using Google's Speech Recognition API. The bot can recognize voice in voice messages, video note messages (videocircles) and audio files.
## Installation
There are two types of installation - standalone and docker (docker compose)
### Standalone
- Clone the repository
```
git clone https://github.com/mrixs/voice-regognision-tg-bot.git
cd telegram-voice-to-text-bot
```
- Install required packages using pip:
```
pip install -r requirements.txt
```
- Configure 
Edit `config.py`. Change the string 
```
BOT_TOKEN = ''  # your bot token from BotFather
``` 
to received by [BotFather](https://t.me/BotFather) string
```
BOT_TOKEN = 'your-bot-token'
```
- Run bot 
```
python main.py
```
### Docker-based (via docker compose)
- Clone the repository
```
git clone https://github.com/mrixs/voice-regognision-tg-bot.git
cd telegram-voice-to-text-bot
```
- Rename `example.env` to `.env` and paste `BOT_TOKEN` received by [BotFather](https://t.me/BotFather)
```
BOT_TOKEN='your-bot-token'
```
- Build image
```
docker compose build
```
- Run bot
```
docker compose up -d
```
## Usage
You can send message to your bot and it replies with recognized text. Also you can add it to group chat. It will recognize all voice messages and replies to it.

If you want to use bot in group chats set privacy to enabled.
In BotFather send `/setprivacy`, select bot and select `Enable`
## License
This software is unlicensed. You can read text of [Unlicense](LICENSE.md)

Other used software are licensed by its own licenses