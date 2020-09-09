# -*- coding: utf-8 -*-
import config
import telebot
import os
import random
import time
from telebot import types
from SQLighter import SQLighter
import utils

bot = telebot.TeleBot(config.token)
k = 1
test = True


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('music/sticker_welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

#   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#   item1 = types.KeyboardButton("Бросить кубик, у кого больше, тот победил:)")
#   item2 = types.KeyboardButton("Угадай мелодию за 10 сек ♫")

#    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, могу играть и общаться.".format(message.from_user, bot.get_me()), parse_mode='html')
    bot.send_message(message.chat.id, "Напишите одну из этих команд \n /dice - сыграть с ботом в кубик \n /game - сыгарть в угадай мелодию за 10 сек ♫")


@bot.message_handler(commands=['dice'])
def cube(message):
    markup_cube = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Играем", callback_data='dice')
    item2 = types.InlineKeyboardButton("Выйти", callback_data='exit')
    markup_cube.add(item1, item2)
    bot.send_message(message.chat.id, "Играем в кости, правила: у кого больше выпало число тот выиграл, удачи",
                     reply_markup=markup_cube)


@bot.callback_query_handler(func=lambda call: True)
def dice(call):
    try:
        if call.message:
            if call.data == 'dice':
                strike_bot = random.randint(0, 6)
                strike_user = random.randint(0, 6)
                if strike_bot > strike_user:
                    answer_dice = "Ты проиграл, удача на моей стороне, только не расстраивайся, повезет в чем-нибудь более важном"
                    answer_dice_r = "Тут был проигрыш"
                elif strike_bot == strike_user:
                    answer_dice = "Одинаково, ну даешь"
                    answer_dice_r = "Тут была ничья"
                else:
                    answer_dice = "Ты выиграл, значит умнее компьютера"
                    answer_dice_r = "Тут была славная победа"
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Бросить еще раз", callback_data='dice')
                item2 = types.InlineKeyboardButton("Выйти", callback_data='exit')
                markup.add(item1, item2)
                bot.send_message(call.message.chat.id,
                     "У тебя выпало " + str(strike_user) + " очков, у меня " + str(strike_bot) + ".\n" + answer_dice,
                     reply_markup=markup)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer_dice_r,
                                      reply_markup=None)
            else:
                bot.send_message(call.message.chat.id, "Вышел:)", reply_markup=None)
    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['game'])
def choice_bd(message):
    markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item1 = types.KeyboardButton("Dopeclvb")
    item2 = types.KeyboardButton("Pharaoh")
    markup1.add(item1, item2)

    bot.send_message(message.chat.id, "Выбери тему музыки", reply_markup=markup1)
#    keyboard_hider = types.ReplyKeyboardRemove()
#    bot.send_message(message.chat.id, "Отлично, погнали!", reply_markup=keyboard_hider)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def game(message):
    global test
    if (message.text == 'Dopeclvb') or (message.text == 'Погнали!'):
        if test:
            game.k = 1
            test = False
        db_worker = SQLighter(config.database_name)
        row = db_worker.select_single(game.k)
        markup = utils.generate_markup(row[2], row[3])
        bot.send_voice(message.chat.id, row[1], reply_markup=markup)
        utils.set_user_game(message.chat.id, row[2])
        db_worker.close()
    elif (message.text == 'Pharaoh') or (message.text == 'Давай следующий!'):
        if test:
            game.k = 1
            test = False
        db_worker = SQLighter(config.database_name)
        row = db_worker.select_single(game.k)
        markup = utils.generate_markup(row[2], row[3])
        bot.send_voice(message.chat.id, row[1], reply_markup=markup)
        utils.set_user_game(message.chat.id, row[2])
        db_worker.close()
    else:
        answer = utils.get_answer_for_user(message.chat.id)
        if not answer:
            bot.send_message(message.chat.id, 'Чтобы начать игру, наберите любую из команд /...')
        else:
            keyboard_hider = types.ReplyKeyboardRemove()
            if message.text == answer:
                bot.send_message(message.chat.id, 'Чертовски правильный ответ', reply_markup=keyboard_hider)
            else:
                bot.send_message(message.chat.id, 'Эх, надо бы подучить треки, неверно', reply_markup=keyboard_hider)
            utils.finish_user_game(message.chat.id)
            markup_d = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            item1_d = types.KeyboardButton('Погнали!')
            item2_d = types.KeyboardButton('Выход:(')
            markup_d.add(item1_d, item2_d)
            if game.k < utils.get_rows_count():
                game.k += 1
                bot.send_message(message.chat.id, 'Готов к следующему треку?', reply_markup=markup_d)
            else:
                bot.send_message(message.chat.id, 'Больше треков нет, выхожу из игры')
                test = True


if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.infinity_polling()
