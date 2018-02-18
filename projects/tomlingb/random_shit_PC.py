#!/usr/bin/env python3

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)


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
    root.bind('<space>', lambda event: send_direction(mqtt_client, "stop"))

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

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=5, column=1)

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker


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
