import telebot
import numpy as np
import torch
import tokens
from funcs import strip_me
import regex as re
from transformers import GPT2LMHeadModel, GPT2Tokenizer

np.random.seed(42)
torch.manual_seed(42)

bot_token = tokens.TOKEN_AvtbusBot
bot_username = tokens.BOT_AvtbusBot
bot = telebot.TeleBot(bot_token)

is_insane = False

MAX_MESSAGE_LENGTH = 4096


def split_message(message):
    return [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! How can I assist you today?")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global is_insane
    if message.chat.type in ['group', 'supergroup']:
        if is_insane:
            response = process_message(message.text)
            bot.reply_to(message, response)
        if f"@{bot_username}" in message.text:
            response = process_message(message.text[len(bot_username) + 2:])
            bot.reply_to(message, response)
    else:
        if tokens.INSANITY_ON in message.text:
            is_insane = True
            bot.reply_to(message, "I\'m INSANE!!!")
            return
        elif tokens.INSANITY_OFF in message.text:
            is_insane = False
            bot.reply_to(message, "I\'m NOT INSANE.")
            return

        response = process_message(message.text)
        bot.reply_to(message, response)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    response = process_message(message.text)
    bot.reply_to(message, response)


# TODO: сделать, чтобы он отвечал на реплаи на себя
def process_message(text):
    text = f"<s>PROMPT: {text}"
    inpt = tok.encode(text, return_tensors="pt")
    out = model.generate(inpt.to(device), max_length=128, repetition_penalty=10.0, do_sample=False,
                         temperature=1)
    return strip_me(tok.decode(out[0]))


def send_response(message, response):
    if response:
        if len(response) > MAX_MESSAGE_LENGTH:
            for chunk in split_message(response):
                bot.reply_to(message, chunk)
        else:
            bot.reply_to(message, response)


tok = GPT2Tokenizer.from_pretrained("models/altbus2")
model = GPT2LMHeadModel.from_pretrained("models/altbus2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

bot.infinity_polling()
