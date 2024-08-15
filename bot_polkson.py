import telebot
import numpy as np
import torch
import tokens
from funcs import strip_me
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer

np.random.seed(42)
torch.manual_seed(42)

bot_token = tokens.TOKEN_PolksonBot
bot_username = tokens.BOT_PolksonBot
bot = telebot.TeleBot(bot_token)

is_insane = False


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
        elif f"@{bot_username}" in message.text:
            response = process_message(message.text[len(bot_username) + 2:])
            bot.reply_to(message, response)
    else:
        # Toggle insanity mode
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


def process_message(text):
    text = f"<s>PROMPT: {text}"
    inpt = tok.encode(text, return_tensors="pt")
    out = model.generate(inpt.to(device), max_length=128, repetition_penalty=10.0, do_sample=False,
                         temperature=1)
    # TODO: сделать capitalize первой буквы сообщения
    return strip_me(tok.decode(out[0]))


tok = GPT2Tokenizer.from_pretrained("models/polkson")
model = GPT2LMHeadModel.from_pretrained("models/polkson")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

bot.infinity_polling()
