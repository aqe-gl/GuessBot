import telebot
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')

bot = telebot.TeleBot(token=BOT_TOKEN)

is_waiting = False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hey. Let's play a game. Think of a number 1-100 and ill guess."
                                      "To start the game use the command: /start_game")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'List of available commands:\n/'
                                      'start - start bot\n'
                                      '/start_game - start game\n'
                                      '/help - see available commands')

@bot.message_handler(commands=['start_game'])
def start_game(message):
    global is_waiting
    is_waiting = True
    bot.send_message(message.chat.id, "Think of a number 1-100 and type 'ready'. Ill try to guess it.")

@bot.message_handler(content_types=['text'])
def answer(message):
    global is_waiting
    if is_waiting and message.text == 'ready':
        pass

bot.polling(non_stop=True, interval=0)