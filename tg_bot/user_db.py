import sqlite3

def ensure_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('user.db') as conn:
            res = func(conn = conn, *args, **kwargs)
        return res

    return inner

@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_mes')

    c.execute('''
    CREATE TABLE IF NOT EXISTS user_mes
    (user_id INTEGER, gr TEXT, class TEXT, date TEXT, time TEXT)
    ''')
    conn.commit()

@ensure_connection
def add_info(conn, user_id: int, gr: str, cl: str, date: str, time: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_mes (user_id, gr, class, date, time) VALUES(?, ?, ?, ?, ?)', (user_id, gr, cl, date, time))
    conn.commit()

@ensure_connection
def check(conn, check_id: int):
    c = conn.cursor()
    c.execute("SELECT user_id FROM user_mes WHERE user_id = ?", (check_id,))
    data = c.fetchall()
    if len(data) == 0:
        return False
    else:
        data = 0
        return True


@ensure_connection
def change_cl(conn, user_id: int, cl: str):
    c = conn.cursor()
    s =''
    c.execute("SELECT date FROM user_mes WHERE user_id = ? and class = ? and gr = ?", (user_id, s, s,))
    g = c.fetchall()
    for i in g:
        if i[0] != '':
            i = i[0]
            c.execute("UPDATE user_mes SET class = ? WHERE user_id = ? and date = ?", (cl, user_id, i, ))
            conn.commit()

@ensure_connection
def stat(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT date FROM user_mes WHERE user_id = ?", (user_id, ))
    date = c.fetchall()
    mes = {}
    for i in date:
        i = i[0]
        if i != '':
            c.execute("SELECT class FROM user_mes WHERE user_id = ? and date = ?", (user_id, i, ))
            g = c.fetchall()
            g = g[0]
            g = g[0]
            mes[i] = g
    return mes

@ensure_connection
def de(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT time FROM user_mes WHERE user_id = ?", (user_id, ))
    g = c.fetchall()
    for i in g:
        i = i[0]
        if i != '':
            c.execute("DELETE FROM user_mes WHERE user_id = ? and time = ?", (user_id, i, ))
            conn.commit()

@ensure_connection
def check_time(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT time FROM user_mes WHERE user_id = ?", (user_id, ))
    g = c.fetchall()
    for i in g:
        i = i[0]
        if i != '':
            return i

@ensure_connection
def get_gr(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT gr FROM user_mes WHERE user_id = ?", (user_id, ))
    g = c.fetchall()
    g = g[0]
    return g[0]
