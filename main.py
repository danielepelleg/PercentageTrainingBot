import os
import dotenv
import telebot

# Load .env variables
dotenv.load_dotenv()
# Global Variables
# global API_KEY
# global bot

class Training:
    def __init__(self, bench_press, deadlift, squat):
        self.bench_press = bench_press
        self.deadlift = deadlift
        self.squat = squat

class Crossfit(Training):
    def __init__(self, bench_press, deadlift, squat, clean, snatch, jerk):
        super().__init__(bench_press, deadlift, squat)
        self.clean = clean
        self.snatch = snatch
        self.jerk = jerk

API_KEY = os.environ.get('API_KEY')
print(API_KEY)

bot = telebot.TeleBot(API_KEY)
print(bot)

@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, """\
        Hi there, I am Example bot.
        What's your name?
        """)

@bot.message_handler(commands=['set'])
def set_rm(message):
    bot.send_message(message.chat.id, 'Imposta qui i tuoi massimali:')
    bot.register_next_step_handler(message, process_bench_step)

def process_bench_step(message):
    try:
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, 'Devi impostare il peso come numero!')
            bot.register_next_step_handler(msg, process_bench_step)
        bot.register_next_step_handler(msg, ...)
    except Exception as e:
        bot.reply_to(message, 'Errore')

bot.polling()
