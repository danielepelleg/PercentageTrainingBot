import os
import dotenv
import telebot

from training import *
from utils import *

# Load .env variables
dotenv.load_dotenv()
# Global Variables
# global API_KEY
# global bot

USER_SESSION = User()
USER_SESSION_DICT = {}

commands = {  # command description used in the "help" command
    'start'       : '\tGet used to the bot',
    'help'        : '\tShow available commands',
    'set'         : '\tSet the training type',
    'exercise'    : '\tChoose the exercise to set',
    'save'        : '\tSave your data in the database'
}

API_KEY = os.environ.get('API_KEY')
print(API_KEY)

bot = telebot.AsyncTeleBot(API_KEY)
print(bot)

@bot.message_handler(commands=['start'])
def greet(message):
    global USER_SESSION
    global USER_SESSION_DICT
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    USER_SESSION = User(user_name, user_id)
    USER_SESSION_DICT = get_user(user_id)
    
    if not USER_SESSION_DICT:
        USER_SESSION_DICT = USER_SESSION.to_dict()
        save_user_data(chat_id, USER_SESSION_DICT)
    else: USER_SESSION.load_from_data(USER_SESSION_DICT)

    bot.send_message(message.chat.id, """\
        Hi there, I am Percentage Training Bot.
        I keep track of your PR's to speed 
            up your training sessions.
        """)

@bot.message_handler(commands=['help'])
def command_help(message):
    chat_id = message.chat.id
    help_text = "⚙️ Commands: \n\n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "• /" + key + " - "
        help_text += commands[key] + "\n"
    bot.send_message(chat_id, help_text)  # send the generated help page

@bot.message_handler(commands=['save'])
def save(message):
    global USER_SESSION_DICT
    chat_id = message.chat.id
    save_user_data(chat_id, USER_SESSION_DICT)
    bot.send_message(chat_id, "User has been saved!")

@bot.message_handler(commands=['set'])
def set_training(message):
    if not USER_SESSION:
        return bot.send_message(message.chat.id, """\
            Use the command /start 
            to begin""")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        telebot.types.InlineKeyboardButton("Powerlifting", callback_data="powerlifting"),
        telebot.types.InlineKeyboardButton("Crossfit", callback_data="crossfit"))

    bot.send_message(message.chat.id, '🏋🏼‍♂️ Choose the training type', reply_markup=markup)

@bot.message_handler(commands=['exercise'])
def set_exercise(message):
    global USER_SESSION
    if USER_SESSION.type == None:
        return bot.send_message(message.chat.id, """\
            Use the command /set to choose 
            the type of training first""")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
            telebot.types.InlineKeyboardButton("Bench Press", callback_data="bench_press"), \
            telebot.types.InlineKeyboardButton("Deadlift", callback_data="deadlift"), \
            telebot.types.InlineKeyboardButton("Squat", callback_data="squat"))
    
    if USER_SESSION.type == "crossfit":
        markup.add(
            telebot.types.InlineKeyboardButton("Clean", callback_data="clean"),
            telebot.types.InlineKeyboardButton("Snatch", callback_data="snatch"),
            telebot.types.InlineKeyboardButton("Jerk", callback_data="jerk"))
    bot.send_message(message.chat.id, '📈 Choose the exercise', reply_markup=markup)

@bot.message_handler(commands=['bench_press', 'deadlift', 'squat', 'clean', 'snatch', 'jerk'])
def greet(message):
    exercise_name = message.text[1:]
    if USER_SESSION.training == None:
        return bot.send_message(message, """\
            Use the command /exercise to choose 
            the set your exercise's PR first""")
    exercise_pr = getattr(USER_SESSION.training, exercise_name)
    table_title = str(exercise_name.upper()).center(17, ' ')
    if exercise_pr != None:
        bot.send_message(message.chat.id, f'**{table_title}**\n{draw_table(int(exercise_pr))}', parse_mode='Markdown')
    else:
        bot.reply_to(message, """\
            Use the command /exercise to choose 
            the set your exercise's PR first""")

@bot.message_handler(commands=['set'])
def set_rm(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(telebot.types.InlineKeyboardButton("Powerlifting", callback_data="powerlifting"),
                               telebot.types.InlineKeyboardButton("Crossfit", callback_data="crossfit"))
    bot.send_message(message.chat.id, 'Choose your type of training', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global USER_SESSION
    global USER_SESSION_DICT
    if call.data == "powerlifting":
        bot.answer_callback_query(call.id, "You chose Powerlifting")
        USER_SESSION.type= "powerlifting"
        USER_SESSION.training = Training()
        USER_SESSION_DICT = USER_SESSION.to_dict()
    elif call.data == "crossfit":
        bot.answer_callback_query(call.id, "You chose Crossfit")
        USER_SESSION.type = "crossfit"
        USER_SESSION.training = Crossfit()
        USER_SESSION_DICT = USER_SESSION.to_dict()
    elif call.data == "bench_press":
        msg = bot.send_message(USER_SESSION.id, 'Insert your 1RM Bench Press:')
        bot.register_next_step_handler(msg, process_bench_step)
    elif call.data == "deadlift":
        msg = bot.send_message(USER_SESSION.id, 'Insert your 1RM Deadlift:')
        bot.register_next_step_handler(msg, process_deadlift_step)
    elif call.data == "squat":
        msg = bot.send_message(USER_SESSION.id, 'Insert your 1RM Squat:')
        bot.register_next_step_handler(msg, process_squat_step)
    elif call.data == "clean":
        msg = bot.send_message(USER_SESSION.id, 'Insert your 1RM Clean:')
        bot.register_next_step_handler(msg, process_clean_step)
    elif call.data == "snatch":
        msg = bot.send_message(USER_SESSION.id, 'Insert your 1RM Snatch:')
        bot.register_next_step_handler(msg, process_snatch_step)
    elif call.data == "jerk":
        msg = bot.send_message(USER_SESSION.id, 'Insert your 1RM Jerk:')
        bot.register_next_step_handler(msg, process_jerk_step)

def process_bench_step(message):
    """ Bench Press Demand
    """
    try:
        global USER_SESSION
        global USER_SESSION_DICT
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_bench_step)
            return
        USER_SESSION.training.bench_press = weight
        USER_SESSION_DICT = USER_SESSION.to_dict()
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_deadlift_step(message):
    """ Deadlift Demand
    """
    try:
        global USER_SESSION
        global USER_SESSION_DICT
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_deadlift_step)
            return
        USER_SESSION.training.deadlift = weight
        USER_SESSION_DICT = USER_SESSION.to_dict()
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_squat_step(message):
    """ Squat Demand
    """
    try:
        global USER_SESSION
        global USER_SESSION_DICT
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_squat_step)
            return
        USER_SESSION.training.squat = weight
        USER_SESSION_DICT = USER_SESSION.to_dict()
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_clean_step(message):
    """ Clean Demand
    """
    try:
        global USER_SESSION
        global USER_SESSION_DICT
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_clean_step)
            return
        USER_SESSION.training.clean = weight
        USER_SESSION_DICT = USER_SESSION.to_dict()
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_snatch_step(message):
    """ Snatch Demand
    """
    global USER_SESSION
    global USER_SESSION_DICT
    try:
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_snatch_step)
            return
        USER_SESSION.training.snatch = weight
        USER_SESSION_DICT = USER_SESSION.to_dict()
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_jerk_step(message):
    """ Jerk Demand
    """
    try:
        global USER_SESSION
        global USER_SESSION_DICT
        chat_id = message.chat.id
        weight = message.text
        if not weight.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_jerk_step)
            return
        USER_SESSION.training.jerk = weight
        USER_SESSION_DICT = USER_SESSION.to_dict()
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

bot.polling()