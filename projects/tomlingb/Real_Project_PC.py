#!/usr/bin/env python3

"""This is the portion of my code that will run the Tkinter window and send instructions to the robot

to see a description of the game go to the ev3 file"""

import tkinter
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import random

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in
        self.color_list = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        self.color_files = ["blue.png", "green.jpg", "yellow.jpg", "red.jpg"]

    def color_submitted(self, color_number):
        file_name = self.color_files[color_number - 2]
        picture_to_display = "{}".format(file_name)
        image = Image.open(picture_to_display)
        image = image.resize((70, 20), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.display_label.configure(image=photo)
        # this method puts the picture corresponding to the color detected by the sensor on the tkinter


def main():
    root = tkinter.Tk()
    root.title("LED Button communication")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_direction(mqtt_client, "forward")
    root.bind('w', lambda event: send_direction(mqtt_client, "forward"))

    backward_button = ttk.Button(main_frame, text='Backward')
    backward_button.grid(row=4, column=1)
    backward_button['command'] = lambda: send_direction(mqtt_client, "backward")
    root.bind('s', lambda event: send_direction(mqtt_client, "backward"))

    left_button = ttk.Button(main_frame, text='Left')
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_direction(mqtt_client, "turn_left")
    root.bind('a', lambda event: send_direction(mqtt_client, "turn_left"))

    right_button = ttk.Button(main_frame, text='Right')
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_direction(mqtt_client, "turn_right")
    root.bind('d', lambda event: send_direction(mqtt_client, "turn_right"))

    stop_button = ttk.Button(main_frame, text='Stop')
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_direction(mqtt_client, "stop")
    root.bind('e', lambda event: send_direction(mqtt_client, "stop"))

    color_button = ttk.Button(main_frame, text='Check Color')
    color_button.grid(row=2, column=4)
    color_button['command'] = lambda: send_check_color(mqtt_client)

    guess_button = ttk.Button(main_frame, text='Submit Color')
    guess_button.grid(row=2, column=5)
    guess_button['command'] = lambda: send_guess(mqtt_client)

    next_turn_button = ttk.Button(main_frame, text='Next')
    next_turn_button.grid(row=4, column=4)
    next_turn_button['command'] = lambda: send_next_turn(mqtt_client)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=6, column=0)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    e_button = ttk.Button(main_frame, text="Exit on EV3 too")
    e_button.grid(row=6, column=2)
    e_button['command'] = lambda: quit_program(mqtt_client, True)

    image = Image.open('blue.png')
    image = image.resize((70, 20), Image.ANTIALIAS)  # this line changes the size of the image to better fit the window
    photo = ImageTk.PhotoImage(image)

    color_label = ttk.Label(main_frame, image=photo)
    color_label.grid(row=3, column=4)

    pc_delegate = MyDelegateOnThePc(color_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
def send_direction(mqtt_client, direction):
    print("Sending direction: {}".format(direction))
    mqtt_client.send_message("move_direction", [direction])


def send_check_color(mqtt_client):
    print("Checking color underneath")
    mqtt_client.send_message("check_color")


def send_guess(mqtt_client):
    print('Submitting')
    mqtt_client.send_message("guess")


def send_next_turn(mqtt_client):
    print('Next_turn')
    mqtt_client.send_message("next_turn")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
