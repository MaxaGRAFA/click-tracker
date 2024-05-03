from pynput import mouse, keyboard

from datetime import datetime

import csv
import json
import sys

import ctypes


class Devices():
    def __init__(self) -> None:
        self.jsonfile = 'data/values.json'
        self.click_coords = 'data/clicking_coords.csv'

        #This is necessary so that the mouse coordinates match the monitor resolution(It is solving scale problem)
        awareness = ctypes.c_int()
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # Saves mouse or button clicks
    def save_press(self, button: str) -> None:
        data = self.load_file()

        # Checks whether such a button already exists
        if data.get(button, False) == False:    
            data[button] = 0

        with open(self.jsonfile, 'w') as jsonFile:
            data[button] = str(int(data[button]) + 1)
            json.dump(data, jsonFile)
        
    # Saves coordinates of the mouse
    def save_coords(self, x: int, y: int, button: mouse.Button) -> None:
        click_time = str(datetime.now())[:-7]

        with open(self.click_coords, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x, y, button, click_time])

    # A function that records information when you click a mouse
    def on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        if pressed:
            self.save_coords(x, y, button)
            self.save_press(str(button))
    
    # Records all keystrokes
    def on_release(self, key: keyboard.Key) -> None:
        self.save_press(str(key).replace("'", ''))

        # f12 is a button for leaving out
        if key == keyboard.Key.f12:
            print('\n\nStopped!')

            self.m_listener.stop() #If I just do sys.exit(0) then m_listener will work, so I stop it
            sys.exit(0)

    # Load a json file 
    def load_file(self) -> dict:
        with open(self.jsonfile, 'r') as jsonFile:
            data = json.load(jsonFile)

        return data

    # Start the programm
    def start_listeners(self):
        with mouse.Listener(on_click=self.on_click) as self.m_listener, \
            keyboard.Listener(on_release=self.on_release) as self.k_listener:
                self.m_listener.join()
                self.k_listener.join()

