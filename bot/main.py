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
    'exercise'    : '\tChoose the exercise to set',
    'tables'      : '\tShow the tables'
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
    user_training = db_mng.get_training(chat_id)
    if not user_training:
        return bot.send_message(chat_id, """\
            Use the command /set to choose 
            the type of training first""")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
            telebot.types.InlineKeyboardButton("Bench Press", callback_data="bench_press"),
            telebot.types.InlineKeyboardButton("Deadlift", callback_data="deadlift"),
            telebot.types.InlineKeyboardButton("Back Squat", callback_data="back_squat"))
    if user_training == "crossfit":
        markup.add(
            telebot.types.InlineKeyboardButton("Clean", callback_data="clean"),
            telebot.types.InlineKeyboardButton("Snatch", callback_data="snatch"),
            telebot.types.InlineKeyboardButton("Jerk", callback_data="jerk"),
            telebot.types.InlineKeyboardButton("Front Squat", callback_data="front_squat"),
            telebot.types.InlineKeyboardButton("Thruster", callback_data="thruster"),
            telebot.types.InlineKeyboardButton("Push Press", callback_data="push_press"),
            telebot.types.InlineKeyboardButton("Shoulder Press", callback_data="shoulder_press"),
            telebot.types.InlineKeyboardButton("Overhead Squat", callback_data="overhead_squat"))
    bot.send_message(chat_id, '📈 Choose the exercise', reply_markup=markup)

@bot.message_handler(commands=['tables'])
def show_tables(message):
    chat_id = message.chat.id
    user_training = db_mng.get_training(chat_id)
    if not user_training:
        return bot.send_message(chat_id, """\
            Use the command /exercise to set 
            your exercise's PR first""")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/bench_press', '/deadlift', '/back_squat')
    if user_training == 'crossfit':
        markup.add('/clean', '/snatch', '/jerk', '/front_squat',
                    '/thruster', '/push_press', '/shoulder_press', '/overhead_squat')
    bot.reply_to(message, 'Choose your PR\'s table', reply_markup=markup)

@bot.message_handler(commands=["bench_press", "deadlift", "back_squat", "clean", 
                                "snatch", "jerk", "front_squat", "thruster", 
                                "push_press", "shoulder_press", "overhead_squat"])
def handle_table(message):
    chat_id = message.chat.id
    exercise_name = str(message.text[1:])
    if not db_mng.get_training(chat_id):
        return bot.send_message(chat_id, """\
            Use the command /exercise to set
            your exercise's PR first""")
    exercise_pr = db_mng.get_exercise(chat_id, exercise_name)
    exercise_name = exercise_name.replace('_', ' ')
    table_title = str(exercise_name.upper()).center(17, ' ')
    if exercise_pr != None:
        bot.send_message(chat_id, f'*{table_title}*\n{draw_table(int(exercise_pr))}', parse_mode='Markdown')
    else:
        bot.reply_to(message, """\
            Use the command /exercise to set
            your exercise's PR first""")

@bot.callback_query_handler(lambda call: call.data in ["powerlifting", "crossfit"])
def callback_query_training(call):
    chat_id = call.message.chat.id
    str_exercise_name = call.data[0].upper() + call.data[1:]
    bot.answer_callback_query(call.id, f"You chose {str_exercise_name}!")
    if not db_mng.get_training(chat_id):
        db_mng.insert_training(chat_id, call.data)
        db_mng.insert_exercise(chat_id)
    else: 
        db_mng.update_training(chat_id, call.data)

@bot.callback_query_handler(lambda call: call.data in ["bench_press", "deadlift", "back_squat", "clean", 
                                                       "snatch", "jerk", "front_squat", "thruster", 
                                                       "push_press", "shoulder_press", "overhead_squat"])
def callback_query_exercise(call):
    chat_id = call.message.chat.id
    exercise = str(call.data).replace('_', ' ').split()
    str_exercise = ' '.join([word[0].upper()+word[1:] for word in exercise])
    bot.send_message(chat_id, f'Insert your 1RM {str_exercise}:')
    bot.register_next_step_handler_by_chat_id(chat_id, process_exercise, str_exercise_name = str_exercise, exercise_name = call.data)

def process_exercise(message, str_exercise_name, exercise_name):
    """ Exercise Demand
    """
    try:
        chat_id = message.chat.id
        exercise_rm = message.text
        if not exercise_rm.isdigit():
            bot.reply_to(message, f'1RM {str_exercise_name} should be a number. Please reinsert')
            bot.register_next_step_handler_by_chat_id(chat_id, process_exercise, str_exercise_name = str_exercise_name, exercise_name = exercise_name)
            return
        db_mng.update_exercise(chat_id, exercise_name, exercise_rm)
        bot.send_message(chat_id, 'Saved!')
    except Exception as e:
        bot.reply_to(message, 'An error occurred')

bot.infinity_polling()