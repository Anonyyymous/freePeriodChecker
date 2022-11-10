import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import Radiobutton

daysOftheWeek = ["monday", "tuesday", "wednesday", "thursday", "friday"]
lessonTimes = [dt.time(1, 0), dt.time(9, 0), dt.time(9, 55), dt.time(10, 50), dt.time(11, 10), dt.time(12, 5),
               dt.time(13, 0), dt.time(13, 55), dt.time(14, 50), dt.time(15, 45), dt.time(16, 40), dt.time(23, 50)]
lessons = ["before school", "period 1", "period 2", "break", "period 3", "period 4", "period 5",
           "period 6", "period 7", "period 8", "after school"]
lesson = 0
weekdayName = ""
weekday = 0
filename = "test.xlsx"
data = pd.read_excel(filename)

mainCanvasIsActive = True
name = ""
dayRadioBtns = []

root = tk.Tk()
root.title = "timetable display"

addPersonCanvas = tk.Canvas(bg="blue")#, height=500, width=500)


def update_lesson():
    now1 = dt.datetime.now()
    now = dt.time(now1.hour, now1.minute)

    global lesson
    for i in range(len(lessonTimes)):
        if lessonTimes[i] > now:
            print(f"now is {now}, or {lessons[i - 1]}")
            lesson = i - 1
            break
    today = dt.date.today()
    global weekdayName
    global weekday
    weekday = today.weekday()
    weekdayName = ""
    if weekday < len(daysOftheWeek):
        weekdayName = daysOftheWeek[weekday]
        print("today is a", weekdayName)


def get_current_next_free():
    update_lesson()
    d = data[weekdayName]
    print(d)
    str = f"{d[lesson]} is free now \n{d[lesson+1]} will be free next period, at " \
          f"{lessonTimes[lesson+1]}".replace("NaN", "no one")
    return str


def get_day():  # TODO
    update_lesson()
    d = data[weekdayName]  # replace the numbers with lessons[num] somehow
    lines = f"{d}".split("\n")

    lines.remove(lines[len(lines)-1])
    for i in range(len(lines)-1):
        x = lines[i].split(" ")
        lines[i] = lessons[i] + x[len(x)-1]
    print(lines)

    str = f"{d}".replace("NaN", "no one")
    print(str)
    return str


def clean_data():
    b = False
    if dayToAdd.get() != "" and periodToAdd != "":
        b = True
    else:
        textBox.delete(0, 'end')
        textBox.insert(0, "select a single day and/or period")
    return b


def view_slot():
    if clean_data():
        day = dayToAdd.get()
        period = lessons.index(periodToAdd.get())
        test = data[day][period]
        textBox.delete(0, 'end')
        textBox.insert(0, f"{test}".replace("nan", "no one"))


def get_name_input():
    if clean_data():
        name = textBox.get()
        day = dayToAdd.get()
        period = lessons.index(periodToAdd.get())
        global data
        data[day][period] = name
        print(name, day, period)
        print(data[day][period])
        data.to_excel(filename)


# removing the random unnecessary columns that appear for some reason
for d in data.columns:
    if "Unnamed" in d:
        data.pop(d)
        print("oh crumbs")
print(data)

s = 0
dayToAdd = tk.StringVar()
for i in daysOftheWeek:
    rb = Radiobutton(addPersonCanvas, text=i, variable=dayToAdd, value=i, width=10, bg="azure3")
    dayRadioBtns.append(rb)
    dayRadioBtns[s].grid(row=s, column=0)
    s += 1
periodToAdd = tk.StringVar()
for i in lessons:
    dayRadioBtns.append(Radiobutton(addPersonCanvas, text=i, variable=periodToAdd, value=i, width=10, bg="azure3"))
    # x = lessons.index(i)
    dayRadioBtns[s].grid(row=s-len(daysOftheWeek), column=1)
    s += 1

textBox = tk.Entry(addPersonCanvas)#, width=30)
textBox.grid(row=s, column=0, columnspan=2)

finishBtn = tk.Button(addPersonCanvas, text="update slot", command=get_name_input)
finishBtn.grid(row=s+1, column=0)

viewSlotBtn = tk.Button(addPersonCanvas, text="view slot", command=view_slot)
viewSlotBtn.grid(row=s+1, column=1)


canvas = tk.Canvas(bg="black")#, height=500, width=500)
canvas.grid(row=0, column=0, rowspan=2)

label = tk.Label(canvas, text="example", bg="azure2")#, height=20, width=40)
label.grid(column=0, row=0, rowspan=2)


def display_now():
    show_default_canvas()
    label.config(text=get_current_next_free())


def display_day():
    show_default_canvas()
    label.config(text=get_day())


def assign_canvas_to_grid(c):
    c.grid(row=0, column=0, rowspan=2)


def toggle_canvas():
    global mainCanvasIsActive
    if mainCanvasIsActive:
        mainCanvasIsActive = False
        # canvas.configure(state="disabled")
        canvas.grid_remove()
        # addPersonCanvas.configure(state="normal")
        assign_canvas_to_grid(addPersonCanvas)
    else:
        show_default_canvas()


def show_default_canvas():
    global mainCanvasIsActive
    mainCanvasIsActive = True
    assign_canvas_to_grid(canvas)
    addPersonCanvas.grid_remove()


# weekdayName = "friday"
# label.config(text=data[weekdayName])
displayDayBtn = tk.Button(text="display day", command=display_day)
displayDayBtn.grid(row=0, column=1)

displayNowBtn = tk.Button(text="display avaliable people", command=display_now)
displayNowBtn.grid(row=1, column=1)

addPersonBtn = tk.Button(text="add someone", command=toggle_canvas)
addPersonBtn.grid(row=2, column=1)

data.to_excel(filename)

root.mainloop()
