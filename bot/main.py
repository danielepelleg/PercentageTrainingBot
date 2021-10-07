import os
import dotenv
import telebot
from telebot import types
from texttable import Texttable

# Load .env variables
dotenv.load_dotenv()
# Global Variables
# global API_KEY
# global bot

user_dict = {}

commands = {  # command description used in the "help" command
    'start'       : '\tGet used to the bot',
    'help'        : '\tShow available commands',
    'set'         : '\tSet the training type',
    'exercise'    : '\tChoose the exercise to set'
}

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.type = None
        self.training = None
    
    def getValue(self):
        if self.training != None:
            return {
                "name": self.name,
                "id": self.id,
                "type": self.type,
                "training": self.training.getValue()
            }
        else:
            return {
                "name": self.name,
                "id": self.id
            }

class Training:
    def __init__(self):
        self.bench_press = None
        self.deadlift = None
        self.squat = None

    # def __init__(self, bench_press, deadlift, squat):
    #     self.bench_press = bench_press
    #     self.deadlift = deadlift
    #     self.squat = squat
    
    def getValue(self):
        return {
            "bench_press": self.bench_press,
            "deadlift": self.deadlift,
            "squat": self.squat
        }

class Crossfit(Training):
    def __init__(self):
        super().__init__()
        self.clean = None
        self.snatch = None
        self.jerk = None

    # def __init__(self, bench_press, deadlift, squat, clean, snatch, jerk):
    #     super().__init__(bench_press, deadlift, squat)
    #     self.clean = clean
    #     self.snatch = snatch
    #     self.jerk = jerk
    
    def getValue(self):
        return {
            "bench_press": self.bench_press,
            "deadlift": self.deadlift,
            "squat": self.squat,
            "clean": self.clean,
            "snatch": self.snatch,
            "jerk": self.snatch
        }

def get_table(number):
    percentages = [50, 55, 60, 63, 66, 68, 70, 73, 75, 78, 80, 82, 85, 88, 90, 95, 98]
    records = [['%', 'Weight']]
    for p in percentages:
        weight = round(float(p*number/100), 2)
        records.append([f'{p}%', f'{weight:.2f}\tKg'])
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.add_rows([row for row in records])
    return f"```{table.draw()}```"

API_KEY = os.environ.get('API_KEY')
print(API_KEY)

bot = telebot.TeleBot(API_KEY)
print(bot)

@bot.message_handler(commands=['start'])
def greet(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    user = User(user_name, user_id)
    user_dict[chat_id] = user
    bot.send_message(message.chat.id, """\
        Hi there, I am Percentage Training Bot.
        I keep track of your PR's to speed 
            up your training sessions.
        """)
    print(user_name, user_id)
    print(user_dict[chat_id].getValue())

@bot.message_handler(commands=['help'])
def command_help(m):
    chat_id = m.chat.id
    help_text = "⚙️ Commands: \n\n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "• /" + key + " - "
        help_text += commands[key] + "\n"
    bot.send_message(chat_id, help_text)  # send the generated help page

@bot.message_handler(commands=['set'])
def set_training(message):
    if not user_dict:
        return bot.send_message(message.chat.id, """\
            Use the command /start 
            to begin""")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(telebot.types.InlineKeyboardButton("Powerlifting", callback_data="powerlifting"),
                               telebot.types.InlineKeyboardButton("Crossfit", callback_data="crossfit"))
    bot.send_message(message.chat.id, '🏋🏼‍♂️ Choose the training type', reply_markup=markup)

@bot.message_handler(commands=['exercise'])
def set_exercise(message):
    user = user_dict[message.chat.id]
    if user.type == None:
        return bot.send_message(message.chat.id, """\
            Use the command /set to choose 
            the type of training first""")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(telebot.types.InlineKeyboardButton("Bench Press", callback_data="bench_press"),
                    telebot.types.InlineKeyboardButton("Deadlift", callback_data="deadlift"),
                    telebot.types.InlineKeyboardButton("Squat", callback_data="squat"))
    if user.type == "crossfit":
        markup.add(telebot.types.InlineKeyboardButton("Clean", callback_data="clean"),
                    telebot.types.InlineKeyboardButton("Snatch", callback_data="snatch"),
                    telebot.types.InlineKeyboardButton("Jerk", callback_data="jerk"))
    bot.send_message(message.chat.id, '📈 Choose the exercise', reply_markup=markup)

@bot.message_handler(commands=['bench_press', 'deadlift', 'squat', 'clean', 'snatch', 'jerk'])
def greet(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    exercise_pr = getattr(user.training, message.text[1:])
    if exercise_pr != None:
        bot.send_message(message.chat.id, get_table(int(exercise_pr)),parse_mode='Markdown')
    else:
        bot.reply_to(message, """\
            Use the /exercise command to set 
            the PR for this exercise first
            """)

@bot.message_handler(commands=['set'])
def set_rm(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(telebot.types.InlineKeyboardButton("Powerlifting", callback_data="powerlifting"),
                               telebot.types.InlineKeyboardButton("Crossfit", callback_data="crossfit"))
    bot.send_message(message.chat.id, 'Choose your type of training', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = user_dict[call.from_user.id]
    if call.data == "powerlifting":
        bot.answer_callback_query(call.id, "You chose Powerlifting")
        user.type = "powerlifting"
        user.training = Training()
    elif call.data == "crossfit":
        bot.answer_callback_query(call.id, "You chose Crossfit")
        user.type = "crossfit"
        user.training = Crossfit()
    elif call.data == "bench_press":
        msg = bot.send_message(user.id, 'Insert your 1RM Bench Press:')
        bot.register_next_step_handler(msg, process_bench_step)
    elif call.data == "deadlift":
        msg = bot.send_message(user.id, 'Insert your 1RM Deadlift:')
        bot.register_next_step_handler(msg, process_deadlift_step)
    elif call.data == "squat":
        msg = bot.send_message(user.id, 'Insert your 1RM Squat:')
        bot.register_next_step_handler(msg, process_deadlift_step)
    elif call.data == "clean":
        msg = bot.send_message(user.id, 'Insert your 1RM Clean:')
        bot.register_next_step_handler(msg, process_clean_step)
    elif call.data == "snatch":
        msg = bot.send_message(user.id, 'Insert your 1RM Snatch:')
        bot.register_next_step_handler(msg, process_snatch_step)
    elif call.data == "jerk":
        msg = bot.send_message(user.id, 'Insert your 1RM Jerk:')
        bot.register_next_step_handler(msg, process_jerk_step)

def process_bench_step(message):
    """ Bench Press Demand
    """
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_bench_step)
            return
        user = user_dict[chat_id]
        user.training.bench_press = weight
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_deadlift_step(message):
    """ Deadlift Demand
    """
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_deadlift_step)
            return
        user = user_dict[chat_id]
        user.training.deadlift = weight
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_squat_step(message):
    """ Squat Demand
    """
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_squat_step)
            return
        user = user_dict[chat_id]
        user.training.squat = weight
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_clean_step(message):
    """ Clean Demand
    """
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_clean_step)
            return
        user = user_dict[chat_id]
        user.training.clean = weight
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_snatch_step(message):
    """ Snatch Demand
    """
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_snatch_step)
            return
        user = user_dict[chat_id]
        user.training.snatch = weight
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_jerk_step(message):
    """ Jerk Demand
    """
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_jerk_step)
            return
        user = user_dict[chat_id]
        user.training.jerk = weight
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

bot.infinity_polling()