import telebot
import traceback
import speech_recognition as sr
import subprocess
import os
import logging
from telebot import types

BOT_TOKEN = None

def read_bot_token():
    try:
        from config import BOT_TOKEN
    except:
        pass

    if len(BOT_TOKEN) == 0:
        BOT_TOKEN = os.environ.get('BOT_TOKEN')

    if BOT_TOKEN is None:
        raise ('Token for the bot must be provided (BOT_TOKEN variable)')
    return BOT_TOKEN

BOT_TOKEN = read_bot_token()

recognizer = sr.Recognizer()
bot = telebot.TeleBot(BOT_TOKEN)

LOG_FOLDER = '.logs'
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename = f'{LOG_FOLDER}/app.log'
)

logger = logging.getLogger('telegram-bot')
logging.getLogger('urllib3.connectionpool').setLevel('INFO')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Welcome! This bot can recognize your *voice* in a voice message and translate '
                                      'it into *text*.' + '\n' +
                     '\n' + 'Send a voice message to start the conversion.', parse_mode='Markdown')


@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    file_id = message.voice.file_id
    file = bot.get_file(file_id)

    file_size = file.file_size
    if int(file_size) >= 5242880: # 5 Megabytes
        bot.send_message(message.chat.id, 'Upload file size is too large.')
    else:
        download_file = bot.download_file(file.file_path)
        with open('audio.ogg', 'wb') as file:
            file.write(download_file)
            subprocess.run(['ffmpeg', '-i', 'audio.ogg', '-vn', 'audio.wav', '-y'])
        recognize_and_reply(message)

@bot.message_handler(content_types=['audio'])
def audio_handler(message):
    file_id = message.audio.file_id
    file = bot.get_file(file_id)

    file_size = file.file_size
    if int(file_size) >= 5242880: # 5 Megabytes
        bot.send_message(message.chat.id, 'Upload file size is too large.')
    else:
        download_file = bot.download_file(file.file_path)  # download file for processing
        with open('audio.mp3', 'wb') as file:
            file.write(download_file)
            subprocess.run(['ffmpeg', '-i', 'audio.mp3', '-vn', 'audio.wav', '-y'])
        recognize_and_reply(message)

@bot.message_handler(content_types=['video_note'])
def video_note_handler(message):
    file_id = message.video_note.file_id
    file = bot.get_file(file_id)

    file_size = file.file_size
    if int(file_size) >= 5242880: # 5 Megabytes
        bot.send_message(message.chat.id, 'Upload file size is too large.')
    else:
        download_file = bot.download_file(file.file_path)  # download file for processing
        with open('audio.mp4', 'wb') as file:
            file.write(download_file)
            subprocess.run(['ffmpeg', '-i', 'audio.mp4', '-vn', 'audio.wav', '-y'])
        recognize_and_reply(message)

def voice_recognizer(language):
    text = 'Words not recognized.'
    file = sr.AudioFile('audio.wav')
    with file as source:
        try:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language)
        except:
            logger.error(f"Exception:\n {traceback.format_exc()}")
    return text

def recognize_and_reply(message):
    text = voice_recognizer('ru_RU')
    bot.reply_to(message, text)
    _clear()

def _clear():
    _files = ['audio.wav', 'audio.ogg']
    for _file in _files:
        if os.path.exists(_file):
            os.remove

if __name__ == '__main__':
    logger.info('start bot')
    bot.polling(True)
    logger.info('stop bot')
