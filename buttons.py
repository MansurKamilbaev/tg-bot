from telebot import types


def phone_number_button():
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number = types.KeyboardButton('Поделиться контактом', request_contact=True)
    button.add(number)
    return button


def main_menu_button(product_from_db):
    button = types.InlineKeyboardMarkup(row_width=2)
    cart = types.InlineKeyboardButton(callback_data='cart', text='Корзина')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}') for i in product_from_db
                    if i[2] > 0]

    button.add(*all_products)
    button.row(cart)
    return button


def choice_product_count(amount=1, plus_or_minus=''):
    button = types.InlineKeyboardMarkup(row_width=3)
    back = types.InlineKeyboardButton(callback_data='back', text='Назад')
    to_cart = types.InlineKeyboardButton(callback_data='to_cart', text='Добавить в корзину')
    plus = types.InlineKeyboardButton(callback_data='plus', text='+')
    minus = types.InlineKeyboardButton(callback_data='minus', text='-')
    count = types.InlineKeyboardButton(callback_data=str(amount), text=str(amount))

    if plus_or_minus == 'plus':
        new_amount = int(amount) + 1
        count = types.InlineKeyboardButton(callback_data=str(new_amount), text=str(new_amount))

    elif plus_or_minus == 'minus':
        if amount > 1:
            new_amount = int(amount) - 1
            count = types.InlineKeyboardButton(callback_data=str(new_amount), text=str(new_amount))

    button.add(minus, count, plus)
    button.row(back, to_cart)
    return button


def cart_button():
    button = types.InlineKeyboardMarkup(row_width=2)
    order = types.InlineKeyboardButton(text='Заказать', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить', callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')

    button.add(order, clear)
    button.row(back)
    return button


def admin_button():
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Добавить концтовар')
    button2 = types.KeyboardButton('Удалить концтовар')
    button3 = types.KeyboardButton('Изменить концтовар')
    button4 = types.KeyboardButton('Вернуться в меню')

    button.add(button1, button2, button3)
    button.row(button4)
    return button


def confirm():
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton('Да')
    button2 = types.KeyboardButton('Нет')

    button.add(button1, button2)
    return button
