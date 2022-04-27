import os
import dotenv
import telebot

from database_manager import *
from utils import *

dotenv.load_dotenv()

db_mng = DBManager()

commands = {  # command description used in the "help" command
    'start'       : '\tGet used to the bot',
    'help'        : '\tShow available commands',
    'set'         : '\tSet the training type',
    'exercise'    : '\tChoose the exercise to set'
}

API_KEY = os.environ.get('API_KEY')
print(API_KEY)

bot = telebot.TeleBot(API_KEY)
print(bot)

@bot.message_handler(commands=['start'])
def greet(message):
    chat_id = message.chat.id
    
    if not db_mng.get_user(chat_id):
        username = message.from_user.first_name
        db_mng.insert_user(chat_id, username)

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

@bot.message_handler(commands=['set'])
def set_training(message):
    chat_id = message.chat.id
    if not db_mng.get_user(chat_id):
        return bot.send_message(message.chat.id, """\
            Use the command /start 
            to begin""")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        telebot.types.InlineKeyboardButton("Powerlifting", callback_data="powerlifting"),
        telebot.types.InlineKeyboardButton("Crossfit", callback_data="crossfit"))

    bot.send_message(chat_id, '🏋🏼‍♂️ Choose the training type', reply_markup=markup)

@bot.message_handler(commands=['exercise'])
def set_exercise(message):
    chat_id = message.chat.id
    if not db_mng.get_training(chat_id):
        return bot.send_message(chat_id, """\
            Use the command /set to choose 
            the type of training first""")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
            telebot.types.InlineKeyboardButton("Bench Press", callback_data="bench_press"), \
            telebot.types.InlineKeyboardButton("Deadlift", callback_data="deadlift"), \
            telebot.types.InlineKeyboardButton("Squat", callback_data="squat"))
    user_training = db_mng.get_training(chat_id)
    if user_training == "crossfit":
        markup.add(
            telebot.types.InlineKeyboardButton("Clean", callback_data="clean"),
            telebot.types.InlineKeyboardButton("Snatch", callback_data="snatch"),
            telebot.types.InlineKeyboardButton("Jerk", callback_data="jerk"))
    bot.send_message(chat_id, '📈 Choose the exercise', reply_markup=markup)

@bot.message_handler(commands=['bench_press', 'deadlift', 'squat', 'clean', 'snatch', 'jerk'])
def handle_exercise(message):
    chat_id = message.chat.id
    exercise_name = str(message.text[1:])
    if not db_mng.get_training(chat_id):
        return bot.send_message(chat_id, """\
            Use the command /exercise to 
            set your exercise's PR first""")
    exercise_pr = db_mng.get_exercise(chat_id, exercise_name)
    exercise_name = exercise_name.replace('_', ' ')
    table_title = str(exercise_name.upper()).center(17, ' ')
    if exercise_pr != None:
        bot.send_message(chat_id, f'**{table_title}**\n{draw_table(int(exercise_pr))}', parse_mode='Markdown')
    else:
        bot.reply_to(message, """\
            Use the command /exercise to
            set your exercise's PR first""")

@bot.callback_query_handler(lambda call: call.data in ["powerlifting", "crossfit"])
def callback_query_training(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id, f"You chose {call.data}!")
    if not db_mng.get_training(chat_id):
        db_mng.insert_training(chat_id, call.data)
        db_mng.insert_exercise(chat_id)
    else: 
        db_mng.update_training(chat_id, call.data)

@bot.callback_query_handler(lambda call: call.data in ["bench_press", "deadlift", "squat", "clean", "snatch", "jerk"])
def callback_query_exercise(call):
    chat_id = call.message.chat.id
    if call.data == "bench_press":
        msg = bot.send_message(chat_id, 'Insert your 1RM Bench Press:')
        bot.register_next_step_handler(msg, process_bench_step)
    elif call.data == "deadlift":
        msg = bot.send_message(chat_id, 'Insert your 1RM Deadlift:')
        bot.register_next_step_handler(msg, process_deadlift_step)
    elif call.data == "squat":
        msg = bot.send_message(chat_id, 'Insert your 1RM Squat:')
        bot.register_next_step_handler(msg, process_squat_step)
    elif call.data == "clean":
        msg = bot.send_message(chat_id, 'Insert your 1RM Clean:')
        bot.register_next_step_handler(msg, process_clean_step)
    elif call.data == "snatch":
        msg = bot.send_message(chat_id, 'Insert your 1RM Snatch:')
        bot.register_next_step_handler(msg, process_snatch_step)
    elif call.data == "jerk":
        msg = bot.send_message(chat_id, 'Insert your 1RM Jerk:')
        bot.register_next_step_handler(msg, process_jerk_step)

def process_bench_step(message):
    """ Bench Press Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_bench_step)
            return
        db_mng.update_exercise(chat_id, 'bench_press', exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_deadlift_step(message):
    """ Deadlift Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_deadlift_step)
            return
        db_mng.update_exercise(chat_id, 'deadlift', exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_squat_step(message):
    """ Squat Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_squat_step)
            return
        db_mng.update_exercise(chat_id, 'squat', exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_clean_step(message):
    """ Clean Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_clean_step)
            return
        db_mng.update_exercise(chat_id, 'clean', exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_snatch_step(message):
    """ Snatch Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_snatch_step)
            return
        db_mng.update_exercise(chat_id, 'snatch', exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

def process_jerk_step(message):
    """ Jerk Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            msg = bot.reply_to(message, '1RM should be a number. Please reinsert')
            bot.register_next_step_handler(msg, process_jerk_step)
            return
        db_mng.update_exercise(chat_id, 'jerk', exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

bot.infinity_polling()