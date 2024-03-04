import telebot
import database
import buttons

bot = telebot.TeleBot('6717597402:AAFWypDJJJHQ-9Yt1_O1xYY8H5dajbdkbwI')
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check_user = database.check_user(user_id)

    if check_user:
        products = database.get_pr_button()
        bot.send_message(user_id, f"Здраствуйте, {message.from_user.first_name}\n"
                                  f"Рады видеть вас обратно в нашем контоварном магазине ",
                         reply_markup=buttons.main_menu_button(products))

    else:
        bot.send_message(user_id, f"Здравствуйте, {message.from_user.first_name}\n"
                                  f"Добро пожаловать в наш концтоварный магазин \n"
                                  f"Давайте регать вас в нашем магазине\n"
                                  f"Пожалуйста отправьте ваше имя")
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    username = message.text
    bot.send_message(user_id, 'Супер! Теперь отправьте номер телефона', reply_markup=buttons.phone_number_button())
    bot.register_next_step_handler(message, get_number, username)


def get_number(message, username):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        database.register_user(user_id, username, phone_number)
        products = database.get_pr_button()
        bot.send_message(user_id, 'Регистрация завершена! Добро пожаловать в магазин концтоваров!',
                         reply_markup=buttons.main_menu_button(products))
    else:
        bot.send_message(user_id, 'Пожалуйста отправьте номер телефона с помощью кнопки',
                         reply_markup=buttons.phone_number_button())
        bot.register_next_step_handler(message, get_number, username)


@bot.callback_query_handler(lambda call: call.data in ['back', 'to_cart', 'plus', 'minus'])
def user_product_count(call):
    chat_id = call.message.chat.id

    if call.data == 'plus':
        count = users[chat_id]['pr_amount']
        users[chat_id]['pr_amount'] += 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choice_product_count(count, 'plus'))

    elif call.data == 'minus':
        count = users[chat_id]['pr_amount']
        users[chat_id]['pr_amount'] -= 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choice_product_count(count, 'plus'))

    elif call.data == 'back':
        products = database.get_pr_button()
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'Вернуть вас в главное меню',
                         reply_markup=buttons.main_menu_button(products))

    elif call.data == 'to_cart':
        products = database.get_product(users[chat_id]['pr_name'])
        product_amount = users[chat_id]['pr_amount']
        user_total = products[4] * product_amount

        database.add_pr_to_cart(chat_id, products[0], product_amount, user_total)
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'концтовары успешно добавлены в корзину', reply_markup=buttons.cart_button())


@bot.callback_query_handler(lambda call: call.data in ['cart', 'back', 'order', 'clear'])
def user_order(call):
    user_id = call.message.from_user.id
    chat_id = call.message.chat.id
    products = database.get_pr_button()
    chat = database.show_cart(chat_id)

    if call.data == 'clear':
        database.delete_from_cart(chat_id)
        bot.edit_message_text('Ваша корзина пуста, выбирайте новые концтовары!', chat_id=chat_id,
                              message_id=call.message.message_id, reply_markup=buttons.main_menu_button(products))

    elif call.data == 'order':
        group_id = -4109841779
        cart = database.make_order(chat_id)
        print(cart)
        order = (f'Новый заказ\n'
                 f'id пользователья: {cart[0][0]}\n'
                 f'концтовар: {cart[0][1]}\n'
                 f'количество: {cart[0][2]}\n'
                 f'цена: {cart[0][3]}\n'
                 f'адрес: {cart[1][0]}\n')
        bot.send_message(group_id, order)
        bot.edit_message_text('Спасибо за ваш Заказ', chat_id=chat_id, message_id=call.message.message_id,
                              reply_markup=buttons.main_menu_button(products))
        print(order)
    elif call.data == 'back':
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'Назад в меню', reply_markup=buttons.main_menu_button(products))

    elif call.data == 'cart':
        check = database.check_cart(user_id)
        if check:
            cart = database.show_cart(chat_id)
            text = (f'Ваша корзинка\n'
                    f'Концтовары: {cart[0]}\n'
                    f'Количества: {cart[1]}\n'
                    f'Цена: {cart[2]}\n'
                    f'Что вы хотите сделать?')
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            bot.send_message(chat, text, reply_markup=buttons.cart_button())

        else:
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            bot.send_message(chat_id, 'Ваша корзинка пуста')


@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_name_id())
def get_user_product(call):
    chat_id = call.message.chat.id
    product = database.get_product(call.data)
    users[chat_id] = {'pr_name': call.data, "pr_amount": 1}
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    text = (f'Название концтовара: {product[0]}\n'
            f'Описание концтовара: {product[1]}\n'
            f'Количество концтовара: {product[2]}\n'
            f'Цена: {product[4]}$')
    bot.send_photo(chat_id, photo=product[3], caption=text, reply_markup=buttons.choice_product_count())


@bot.message_handler(commands=['admin'])
def action(message):
    admin_id = 948270079
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Что хотите сделать?', reply_markup=buttons.admin_button())
        bot.register_next_step_handler(message, admin_choice)

    else:
        bot.send_message(message.from_user.id, 'Вы не являетесь админом')


def admin_choice(message):
    admin_id = 948270079
    if message.text == 'Добавить концтовар':
        bot.send_message(admin_id, 'Введите название концтовара',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, get_pr_name)

    elif message.text == 'Удалить концтовар':
        check = database.check_product()
        if check:
            bot.send_message(admin_id, 'Введите Ид концтовара',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_pr_id)
        else:
            bot.send_message(admin_id, 'концтовар не существует в базе')
            bot.register_next_step_handler(message, admin_choice)

    elif message.text == 'Изменить концтовар':
        check = database.check_product()
        if check:
            bot.send_message(admin_id, 'Введите Ид концтовара',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_pr_change)
        else:
            bot.send_message(admin_id, 'концтовар не существует в базе', )
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Вернуться в меню':
        products = database.get_pr_button()
        bot.send_message(admin_id, 'Добро пожаловать в меню!',
                         reply_markup=buttons.main_menu_button(products))
    else:
        bot.send_message(admin_id, 'Неправильная команда!', reply_markup=buttons.admin_button())
        bot.register_next_step_handler(message, admin_choice)


def get_pr_name(message):
    admin_id = 948270079
    if message.text:
        product_name = message.text
        bot.send_message(admin_id, 'Отлично, Отправьте описание концтовара')
        bot.register_next_step_handler(message, get_pr_desc, product_name)

    else:
        bot.send_message(admin_id, 'Отправьте в текстовом формате')
        bot.register_next_step_handler(message, get_pr_name)


def get_pr_desc(message, product_name):
    admin_id = 948270079
    if message.text:
        pr_desc = message.text
        bot.send_message(admin_id, 'Отправьте количество концтовра')
        # Step to get count for product
        bot.register_next_step_handler(message, get_pr_count, product_name, pr_desc)
    else:
        bot.send_message(admin_id, 'Отправьте описание в текстовом формате')
        bot.register_next_step_handler(message, get_pr_desc, product_name)


def get_pr_count(message, product_name, pr_desc):
    admin_id = 948270079
    pr_count = int(message.text)
    bot.send_message(admin_id,
                     'Теперь переходите на сайт: https://postimages.org/ru/ , и загрузите фото продукта и отправьте линк в бота')
    bot.register_next_step_handler(message, get_pr_image, product_name, pr_desc, pr_count)


def get_pr_image(message, product_name, pr_desc, pr_count):
    admin_id = 948270079
    if message.text:
        pr_photo = message.text
        bot.send_message(admin_id, 'Отлично теперь  отправьте цену концтовара?')
        bot.register_next_step_handler(message, get_pr_cost, product_name, pr_desc, pr_count, pr_photo)


def get_pr_cost(message, pr_name, pr_des, pr_count, pr_photo):
    admin_id = 948270079
    pr_price = float(message.text)
    database.add_product(pr_name, pr_des, pr_count, pr_photo, pr_price)
    bot.send_message(admin_id, 'концтовар добавлен', reply_markup=buttons.admin_button())
    bot.register_next_step_handler(message, admin_choice)


def get_pr_id(message):
    admin_id = 948270079

    pr_id = int(message.text)
    database.check_product_id(pr_id)
    database.delete_pr(pr_id)
    bot.send_message(admin_id, 'концтовар удален', reply_markup=buttons.admin_button())
    bot.register_next_step_handler(message, admin_choice)


def get_pr_change(message):
    admin_id = 948270079

    pr_id = int(message.text)
    check = database.check_product_id(pr_id)
    if check:
        bot.send_message(admin_id, 'Сколько концтоваров', reply_markup=buttons.admin_button())
        # Step "how many came"
        bot.register_next_step_handler(message, get_amount, pr_id)
    else:
        bot.send_message(admin_id, 'Этот концтовара нету в базе')
        # Return to function
        bot.register_next_step_handler(message, get_pr_change)


def get_amount(message, pr_id):
    admin_id = 948270079
    new_amount = int(message.text)
    database.change_pr_count(pr_id, new_amount)
    bot.send_message(admin_id, 'Количество концтовара изменено')
    bot.register_next_step_handler(message, admin_choice)


bot.infinity_polling()
