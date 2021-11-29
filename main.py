import json
import os
import time
import webbrowser as window
from tkinter import *

from nikkiepy.files import mkfile
from pynput.mouse import Button as mb
from pynput.mouse import Controller as mc
from pynput.mouse import Listener as ml

mouse = mc()

click_count = 0
clicking = False

def open_site():
    print("Opening website")
    window.open("https://nikkiedev.com")

def start_clicking():
    global clicking
    global click_count

    with open("user data/settings.json", 'r') as f:
        settings_file = json.load(f)
    
    mouse_x = settings_file["mouse_x"]
    mouse_y = settings_file["mouse_y"]

    print(f"Moving mouse to X: {mouse_x} Y: {mouse_y}")
    mouse.position = (mouse_x, mouse_y)
    print("Clicking...")
    clicking = True
    
    while clicking == True:
        mouse.click(mb.left)
        click_count = click_count + 1
        print(f"Clicked, count: {click_count}")
        time.sleep(settings_file["click_interval"])


        if (click_count == settings_file["click_limit"]):
            clicking = False
            print("Stopped clicking")
            print("Total times clicked: {0}".format(click_count))
            click_count = 0

def main():
    global clicking

    print("Home")
    os.system("cls")

    print("NikkieDev - Auto Clicker")
    print("Windows version 0.1.0")
    print("https://nikkiedev.com")

    win = Tk()
    win.geometry("640x480")
    win.resizable(0,0)
    win.title("Auto Clicker - Home")
    win.config(bg="grey12")

    def open_settings():
        win.destroy()
        print("Settings")

        set_win = Tk()
        set_win.geometry("640x480")
        set_win.resizable(0,0)
        set_win.title("Auto Clicker - Settings")
        set_win.config(bg="grey12")

        header = Label(set_win, text="Settings", font=("arial", 16), fg="white", bg="grey12")
        header.place(x=260, y=5)

        limit_label = Label(set_win, text="Click limit: ", font=("arial", 16), fg="white", bg="grey12")
        limit_label.place(x=180, y=120)
        interval_label = Label(set_win, text="Click interval: ", font=("arial", 16), fg="white", bg="grey12")
        interval_label.place(x=150, y=160)

        limit_entry = Entry(set_win, width=25)
        limit_entry.place(x=290, y=120)
        interval_entry = Entry(set_win, width=25)
        interval_entry.place(x=290, y=160)

        with open("user data/settings.json", "r") as f:
            settings_file = json.load(f)

        limit = settings_file["click_limit"]
        interval = settings_file["click_interval"]

        limit_entry.insert(0, limit)
        interval_entry.insert(0, interval)

        def apply_new_settings():

            with open("user data/settings.json", "r") as f:
                settings_file = json.load(f)

            settings_file["click_limit"] = int(limit_entry.get())
            settings_file["click_interval"] = float(interval_entry.get())

            if settings_file["click_interval"] is None:
                settings_file["click_interval"] = float(0.5)

            elif settings_file["click_limit"] is None:
                settings_file["click_limit"] = int(50)

            with open("user data/settings.json", "w") as f:
                json.dump(settings_file, f, indent=4)

            set_win.destroy()
            main()

        apply_btn = Button(set_win, text="Apply", font=("arial", 12), bg="grey95", fg="black", bd=5, relief=RAISED, width=15, command=apply_new_settings)
        apply_btn.place(x=250, y=250)

    header = Label(win, text="Auto Clicker", font=("arial", 16), fg="white", bg="grey12")
    header.place(x=260,y=5)
    madeby = Label(win, text="Made by: Nik Schaad", font=("arial", 7), fg="white", bg="grey12")
    madeby.place(x=535, y=460)

    wb_btn = Button(win, text="Website", font=("arial", 12), bg="grey95", fg="black", bd=5, relief=RAISED, width=15, command=open_site)
    wb_btn.place(x=150, y=160)
    settings_btn = Button(win, text="Settings", font=("arial", 12), bg="grey95", fg="black", bd=5, relief=RAISED, width=15, command=open_settings)
    settings_btn.place(x=375, y=160)
    clicking_btn = Button(win, text="Start", font=("arial", 12), bg="grey95", fg="black", bd=5, relief=RAISED, width=15, command=start_clicking)
    clicking_btn.place(x=240, y=250)

    with open("user data/settings.json", "r") as f:
        settings_file = json.load(f)

    set_x = settings_file["mouse_x"]
    set_y = settings_file["mouse_y"]

    position = Entry(win, width=25)
    position.insert(0, f"X: {set_x}, Y: {set_y}")
    position.place(x=250, y=385)

    def get_mouse_pos():
        def on_click(x, y, button, pressed):
            print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
            if not pressed:
                return False

            position.delete(0, END)
            position.insert(0, f"X: {x}, Y: {y}")

            set_x = x
            set_y = y

            with open("user data/settings.json", "r") as f:
                settings_file = json.load(f)

            settings_file["mouse_x"] = set_x
            settings_file["mouse_y"] = set_y

            with open("user data/settings.json", "w") as f:
                json.dump(settings_file, f, indent=4)
        
        ml(on_click=on_click).start()

    scan_button = Button(win, text="Scan mouse position", font=("arial", 12), bg="grey95", fg="black", bd=5, relief=RAISED, width=25, command=get_mouse_pos)
    scan_button.place(x=220, y=325)

    pos_label = Label(win, text="Mouse position: ", font=("arial", 16), fg="white", bg="grey12")
    pos_label.place(x=90, y=380)

    win.mainloop()

main()
os.system("cls")
