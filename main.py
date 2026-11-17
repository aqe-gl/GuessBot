import telebot
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')

bot = telebot.TeleBot(token=BOT_TOKEN)

is_waiting = False
bot_number = None
left = None # start of range
right = None # end of range

def middle(left, right):
    return int((right - left) / 2 + left)

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
    global is_waiting, left, right
    is_waiting = True
    bot.send_message(message.chat.id, "Whats the smallest number you can think of?")

@bot.message_handler(content_types=['text'])
def answer(message):
    global is_waiting, bot_number, left, right
    if is_waiting and message.text == 'ready':
        bot_number = middle(left, right)
        bot.send_message(message.chat.id, f"Im thinking it is: {bot_number}. Type '>' or '<' or '='.")
        is_waiting = False
    elif message.text == '<' and bot_number is not None:
        right = bot_number - 1
        bot_number = middle(left, right)
        bot.send_message(message.chat.id, f"Im thinking it is: {bot_number}. Type '>' or '<' or '='.")
    elif message.text == '>' and bot_number is not None:
        left =  bot_number + 1
        bot_number = middle(left, right)
        bot.send_message(message.chat.id, f"Im thinking it is: {bot_number}. Type '>' or '<' or '='.")
    elif message.text == '=' and bot_number is not None:
        left = None
        right = None
        bot.send_message(message.chat.id, f"Hooray I guessed it! To start new game type /start_game")
        bot_number = None
    elif message.text.isdigit() and left is None:
        left = int(message.text)
        bot.send_message(message.chat.id, "Whats the biggest number you can think of?")
    elif message.text.isdigit() and right is None:
        right = int(message.text)
        bot.send_message(message.chat.id, f"Think of a number {left}-{right} and type 'ready'. Ill try to guess it.")

    else:
        bot.send_message(message.chat.id, f"To start new game type /start_game")

bot.polling(non_stop=True, interval=0)