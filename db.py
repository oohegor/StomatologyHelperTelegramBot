import sqlite3


# Stream secure database connection
def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('bot.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Check that the necessary tables exist, otherwise create them
         Important: you must migrate to such tables yourself!

    :param conn: connection to a DBMS
    :param force: explicitly recreate all tables
    """
    c = conn.cursor()

    # Doctors clients information
    if force:
        c.execute('DROP TABLE IF EXISTS doctors_clients')

    c.execute('''
        CREATE TABLE IF NOT EXISTS doctors_clients (
            id                     INTEGER PRIMARY KEY,
            telegram_user_id       INTEGER NOT NULL,
            username               TEXT NOT NULL,
            appointment_date       TEXT DEFAULT NULL
        )
    ''')

    # Save changes
    conn.commit()


@ensure_connection
def select_clients(conn):
    c = conn.cursor()
    c.execute('SELECT telegram_user_id, username, appointment_date FROM doctors_clients')
    return c.fetchall()


@ensure_connection
def add_client(conn, telegram_user_id: int, username: str, appointment_date: str):
    c = conn.cursor()
    c.execute(
        'INSERT INTO doctors_clients (telegram_user_id, username, appointment_date) VALUES (?, ?, ?)',
        (telegram_user_id, username, appointment_date)
    )

    conn.commit()


@ensure_connection
def delete_client(conn, telegram_user_id: int):
    c = conn.cursor()
    c.execute('DELETE FROM doctors_clients WHERE telegram_user_id = ?', (telegram_user_id,))

    conn.commit()

# If you need to create a database, run this script once
# if __name__ == '__main__':
#     init_db()
#     add_client(telegram_user_id='123321', username='egor', appointment_date='01/01/1990')
#     r = select_clients()
#     print(r)
