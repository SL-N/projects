import sqlite3

def ensure_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('schedule.db') as conn:
            res = func(conn = conn, *args, **kwargs)
        return res

    return inner

@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS schedule')

    c.execute('''
    CREATE TABLE IF NOT EXISTS schedule
    (gr TEXT, m TEXT, t TEXT, w TEXT, th TEXT, f TEXT, s TEXT)
    ''')
    conn.commit()

@ensure_connection
def set(conn, number, m, t, w, th, f, s):
    c = conn.cursor()
    c.execute('INSERT INTO schedule (gr, m, t, w, th, f, s) VALUES(?, ?, ?, ?, ?, ?, ?)', (number, m, t, w, th, f, s, ))
    conn.commit()

@ensure_connection
def get_schedule(conn, number, day):
    c = conn.cursor()
    if day == 'Понедельник':
        c.execute("SELECT m FROM schedule WHERE gr = ?", (number, ))
    elif day == 'Вторник':
        c.execute("SELECT t FROM schedule WHERE gr = ?", (number, ))
    elif day == 'Среда':
        c.execute("SELECT w FROM schedule WHERE gr = ?", (number, ))
    elif day == 'Четверг':
        c.execute("SELECT th FROM schedule WHERE gr = ?", (number, ))
    elif day == 'Пятница':
        c.execute("SELECT f FROM schedule WHERE gr = ?", (number, ))
    else:
        c.execute("SELECT s FROM schedule WHERE gr = ?", (number, ))
    g = c.fetchall()
    print(g)
    g = g[0]
    g = g[0]
    return g
