import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
import os
import socket
from datetime import datetime
import netifaces as ni
from requests import get

TOKEN = '1733508097:AAFrnvM4UW7jJDJ_U_pqUoDb53cEZ8MLVok'

bot = telebot.TeleBot(TOKEN)
chat_id = 470087443
bot.last_message_sent = {}
now = datetime.now()


@bot.message_handler(commands=['start'], func=lambda message: True)
def send_message(message):
    msg = bot.send_message(message.chat.id, "<b>Benvenuto sul bot!</b> \U0001F916"
                                            "\n\nCliccando sui bottoni sottostanti puoi vedere l'elenco di tutte le "
                                            "funzioni del bot e le informazioni principali su esso",
                           parse_mode='HTML', reply_markup=start_markup())
    bot.last_message_sent = msg.chat.id, msg.message_id


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Funzionalità  \U0001F4BB", callback_data="cb_function"),
               InlineKeyboardButton("Info Bot  \u2139\uFE0F", callback_data="cb_info"))
    return markup


def indietro_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("\U0001f519 Indietro", callback_data="cb_indietro"))
    return markup


def profilo_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("\U0001f464 Info sul Creatore", url="http://127.0.0.1:8080"),
               InlineKeyboardButton("\U0001f519 Indietro", callback_data="cb_indietro"))
    return markup


def function_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("\u2601\uFE0F  Sito ", url="http://127.0.0.1:8082"),
               InlineKeyboardButton("\U0001f4dc  Wiki", url="http://127.0.0.1/wiki/doku.php?id=progetto"))
    markup.add(InlineKeyboardButton("\U0001f527  Gestione del Raspberry", callback_data="cb_gest_rasp"))
    markup.add(InlineKeyboardButton("\U0001f519  Indietro", callback_data="cb_indietro"))
    return markup


def gestione_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("\u25B6\uFE0F  Reboot", callback_data="cb_reboot"),
               InlineKeyboardButton("\U0001f504  Update", callback_data="cb_update"))
    markup.add(InlineKeyboardButton("\U0001f519  Indietro", callback_data="cb_indietro"))
    return markup


def get_Host_name_IP():
    try:
        bot.send_message(chat_id, text="<b>Riavvio completato!</b>", parse_mode='HTML')
        host_name = socket.gethostname()
        list_ip = ""
        for x in ni.interfaces():
            ip = ni.ifaddresses(x)[ni.AF_INET][0]['addr']
            list_ip += "\n" + x + ": " + ip
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        host_name_ip = "\u2122\uFE0F  Hostname: " + str(host_name) + "\n\u2601\uFE0F  IP: " + list_ip + \
                       "\n\U0001f4c5  Data e ora: " + str(dt_string)
        bot.send_message(chat_id, text=host_name_ip)
    except Exception as err:
        bot.send_message(chat_id, text=err)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_function":
        bot.delete_message(*bot.last_message_sent)
        msg = bot.send_message(chat_id, text="<b>Cosa puoi fare con il bot?:</b>"
                                             "\n\n\U0001f310 <b>Sito web:</b> visualizzare la guida per "
                                             "la configurazione di un Raspberry PI"
                                             "\n\U0001f4da <b>Wiki:</b> visualizzare l'enciclopedia sul Raspberry"
                                             "\n\u2699\uFE0F <b>Gestione:</b> è possibile gestire le impostazioni "
                                             "principali del Raspberry direttamente da Telegram",
                               parse_mode='HTML', reply_markup=function_markup())
        bot.last_message_sent = msg.chat.id, msg.message_id
    elif call.data == "cb_info":
        bot.delete_message(*bot.last_message_sent)
        msg = bot.send_message(chat_id, text="<b>Informazioni sul bot:</b>"
                                             "\n\n\U0001f464 <b>Creatore:</b> @Trapp_99"
                                             "\n\U0001f5fa\uFE0F <b>Lingua:</b>  Italiano \U0001f1ee\U0001f1f9 "
                                             "\n\U0001f4f1 <b>Supporto inline:</b> No"
                                             "\n\U0001f465 <b>Utilizzo nei gruppi:</b> No"
                                             "\n\u2139\uFE0F <b>Descrizione:</b> bot per comunicare "
                                             "con il proprio Raspberry PI ",
                               parse_mode='HTML', reply_markup=profilo_markup())
        bot.last_message_sent = msg.chat.id, msg.message_id
    elif call.data == "cb_indietro":
        bot.delete_message(*bot.last_message_sent)
        msg = bot.send_message(chat_id, text="<b>Benvenuto sul bot!</b> \U0001F916"
                                             "\n\nPremi i bottoni sotto per vedere la lista dei comandi"
                                             " e le informazioni sul bot",
                               parse_mode='HTML', reply_markup=start_markup())
        bot.last_message_sent = msg.chat.id, msg.message_id
    elif call.data == "cb_gest_rasp":
        bot.delete_message(*bot.last_message_sent)
        msg = bot.send_message(chat_id, text="<b>\U0001f6e0\uFE0F Benvenuto nel menù di gestione del Raspberry!</b>"
                                             "\n\n\U0001f4cc Cliccando sui bottoni sottostanti potrai eseguire "
                                             "diverse azioni che ti velocizzeranno alcuni processi nella "
                                             "gestione della tua rete.",
                               parse_mode='HTML', reply_markup=gestione_markup())
        bot.last_message_sent = msg.chat.id, msg.message_id
    elif call.data == "cb_update":
        bot.delete_message(*bot.last_message_sent)
        msg = bot.send_message(chat_id, text="Aggiornamento dei pacchetti iniziato...")
        bot.last_message_sent = msg.chat.id, msg.message_id
        os.system('sudo apt-get update')
        if subprocess.CompletedProcess:
            bot.delete_message(*bot.last_message_sent)
            msg = bot.send_message(chat_id, text="Aggiornamento completato",
                                   reply_markup=indietro_markup())
            bot.last_message_sent = msg.chat.id, msg.message_id
    elif call.data == "cb_reboot":
        bot.delete_message(*bot.last_message_sent)
        msg = bot.send_message(chat_id, text="Riavvio iniziato...")
        bot.last_message_sent = msg.chat.id, msg.message_id
        os.system('sudo reboot')


get_Host_name_IP()
bot.polling(none_stop=True)
