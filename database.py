import sqlite3

conn = sqlite3.connect('users.db', check_same_thread=False)

sql = conn.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, phone_number TEXT);')

sql.execute(
    'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_desc TEXT, '
    'pr_count INTEGER,'
    'pr_image TEXT, pr_price REAL);')

sql.execute('CREATE TABLE IF NOT EXISTS user_cart (user_id INTEGER, user_product TEXT, pr_amount INTEGER, '
            'total_for_price REAL);')


def register_user(tg_id, name, phone_number):
    sql.execute('INSERT INTO users(id, username, phone_number) VALUES (?, ?, ?);', (tg_id, name, phone_number))
    conn.commit()


# Ваш остальной код без изменений

def check_user(tg_id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    checker = sql.execute('SELECT id FROM users WHERE id=?;', (tg_id,))

    if checker.fetchone():
        return True
    else:
        return False


def add_product(pr_name, pr_desc, pr_count, pr_photo, pr_price):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    sql.execute('INSERT INTO  products(pr_name, pr_desc, pr_count, pr_image, pr_price) VALUES(?, ?, ?, ?, ?);',
                (pr_name, pr_desc, pr_count, pr_photo, pr_price))

    conn.commit()


def get_product(id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    result = sql.execute('SELECT pr_name, pr_desc, pr_count, pr_image, pr_price FROM products WHERE id=?;', (id,))
    return result.fetchone()


def get_pr_button():
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    return sql.execute('SELECT id, pr_name, pr_count FROM products;').fetchall()


def delete_pr(id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    sql.execute('DELETE FROM products WHERE id=?;', (id,))

    conn.commit()


def change_pr_count(id, new_count):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    new_count = sql.execute('SELECT pr_count FROM products WHERE id=?;', (id,)).fetchall()

    add_to_new_count = new_count[0] + new_count
    sql.execute('UPDATE products SET pr_count=? WHERE id=?;', (add_to_new_count, id))


def get_pr_name_id():
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    products = sql.execute('SELECT id, pr_count FROM products;').fetchall()
    sorted_products = [(i[0]) for i in products if i[1] > 0]
    return sorted_products


def check_product():
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    if sql.execute('SELECT * FROM products;').fetchall():
        return True
    else:
        return False


def check_product_id(id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    if sql.execute('SELECT id FROM products WHERE id=?;', (id,)).fetchone():
        return True
    else:
        return False


def add_pr_to_cart(user_id, user_product, pr_amount, total_for_price):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    sql.execute('INSERT INTO user_cart VALUES(?, ?, ?, ?);', (user_id, user_product, pr_amount, total_for_price))

    conn.commit()


def delete_from_cart(user_id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    sql.execute('DELETE FROM user_cart WHERE user_id=?;', (user_id,))

    conn.commit()


def check_cart(id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    if sql.execute('SELECT user_product FROM user_cart WHERE user_id=?;', (id,)).fetchall():
        return True
    else:
        return False


def make_order(user_id):
    conn = sqlite3.connect('users.db')

    sql = conn.cursor()

    pr_name = sql.execute('SELECT user_product FROM user_cart WHERE user_id=?;', (user_id,)).fetchone()
    amount = sql.execute('SELECT pr_amount FROM user_cart WHERE user_id=?;', (user_id,)).fetchone()
    pr_count = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (pr_name[0],)).fetchone()
    new_count = pr_count[0] - amount[0]
    sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (new_count, pr_name[0]))
    information = sql.execute('SELECT * FROM user_cart WHERE user_id=?;', (user_id,)).fetchone()
    address = sql.execute('SELECT address FROM users WHERE id=?;', (user_id,)).fetchone()

    conn.commit()
    return information, address


def show_cart(user_id):
    return sql.execute('SELECT user_product, pr_amount, total_for_price FROM user_cart WHERE user_id=?;',
                       (user_id,)).fetchone()
