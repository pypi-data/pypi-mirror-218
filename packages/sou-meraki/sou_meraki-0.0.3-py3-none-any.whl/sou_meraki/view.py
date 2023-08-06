#!/usr/bin/env python3

"""Used to present the view to the user
"""

import os
import platform


MENU_TITLE = """
   ____          _   _         __  __                     _     _ 
  / ___|   ___  | | | |       |  \/  |  ___  _ __   __ _ | | __(_)
  \___ \  / _ \ | | | | _____ | |\/| | / _ \| '__| / _` || |/ /| |
   ___) || (_) || |_| ||_____|| |  | ||  __/| |   | (_| ||   < | |
  |____/  \___/  \___/        |_|  |_| \___||_|    \__,_||_|\_\|_|
"""

def clear_screen():
    if(platform.system().lower()=='windows'):
        cmd = 'cls'
    else:
        cmd = 'clear'
    os.system(cmd)


def display_menu(menu):
    clear_screen()
    print(f"\033[38;2;245;90;66m{MENU_TITLE}\033[0m")
    for k, v in menu.items():
        colortext = f"    \033[38;2;90;200;66m{k} - {v['description']}\033[0m"
        print(colortext)


def display_error(msg):
    clear_screen()
    print(f"\n\033[38;2;245;90;66m  ERROR: {msg}\033[0m")

