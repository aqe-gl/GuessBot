import telebot
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')

bot = telebot.TeleBot(token=BOT_TOKEN)

is_waiting = False
bot_number = None

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
    global is_waiting, bot_number
    if is_waiting and message.text == 'ready':
        bot_number = 1
        bot.send_message(message.chat.id, f"Im thinking it is: {bot_number}. Type 'yes' or 'no'.")
        is_waiting = False
    elif message.text == 'no' and bot_number is not None:
        bot_number += 1
        bot.send_message(message.chat.id, f"Im thinking it is: {bot_number}. Type 'yes' or 'no'.")
    elif message.text == 'yes' and bot_number is not None:
        bot.send_message(message.chat.id, f"Hooray I guessed it! To start new game type /start_game")
        bot_number = None
    else:
        bot.send_message(message.chat.id, f"To start new game type /start_game")

bot.polling(non_stop=True, interval=0)