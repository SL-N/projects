import openpyxl
from Group import Group
from Group import DaysOfTheWeek
from schedule_db import set, init_db

def main(count):
    schedule = openpyxl.open("tab.xlsx", read_only=True)
    sheet = schedule.active
    number = sheet[2][count].value
    daysOfTheWeek = []
    q = 1
    for i in range(6):
        lessons = []
        for j in range(7):
            if (sheet[2 + q][count].value != None):
                lessons.append(sheet[2 + q][count].value)
            else:
                lessons.append("")
            q = q + 1

        daysOfTheWeek.append(lessons)
    group = Group(number, daysOfTheWeek[0], daysOfTheWeek[1], daysOfTheWeek[2], daysOfTheWeek[3], daysOfTheWeek[4],
                          daysOfTheWeek[5])
    return group


init_db()
for i in range(3, 59):
    gr = main(i)
    set(number = str(gr.number), m = str(gr.dayOfTheWeek1), t = str(gr.dayOfTheWeek2), w = str(gr.dayOfTheWeek3), th = str(gr.dayOfTheWeek4),
               f = str(gr.dayOfTheWeek5), s = str(gr.dayOfTheWeek6))
