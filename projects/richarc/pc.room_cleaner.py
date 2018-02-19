import tkinter
from tkinter import ttk
from tkinter import *

import mqtt_remote_method_calls as com
import time


class MyDelegateOnThePc(object):

    def __init__(self, room_status_label):
        self.room_status_label = room_status_label

    def message_from_ev3(self, blue_position, orange_position):
        if blue_position == 'Found':
            if orange_position == 'Found':
                self.room_status_label.configure(text="Blue and Orange needs to be organized.")
            if orange_position == 'Home':
                self.room_status_label.configure(text="Blue needs to be organized, Orange is organized.")
            if orange_position == 'Missing':
                self.room_status_label.configure(text="Blue needs to be organized, Orange is missing.")
        elif blue_position == 'Home':
            if orange_position == 'Found':
                self.room_status_label.configure(text="Blue is organized, Orange needs to be organized.")
            if orange_position == 'Home':
                self.room_status_label.configure(text="Blue and Orange are organized.")
            if orange_position == 'Missing':
                self.room_status_label.configure(text="Blue is organized, Orange is missing.")
        else:
            if orange_position == 'Found':
                self.room_status_label.configure(text="Blue is missing, Orange needs to be organized.")
            if orange_position == 'Home':
                self.room_status_label.configure(text="Blue is missing, Orange is organized.")
            if orange_position == 'Missing':
                self.room_status_label.configure(text="Blue and Orange are missing.")


def main():
    root = tkinter.Tk()
    root.title("Organizer")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    status_label = tkinter.Label(main_frame, text="Current Status:")
    status_label.grid(row=0, column=1, sticky=S)

    message_label = ttk.Label(main_frame, text="--")
    message_label.grid(row=1, column=1)

    check_status_button = ttk.Button(main_frame, text="Check Status")
    check_status_button.grid(row=3, column=1)
    check_status_button['command'] = lambda: send_check_area(mqtt_client)

    organize_label = tkinter.Label(main_frame, text="Organizer Options:", wraplength=60)
    organize_label.grid(row=0, column=0)

    blue_checkbox_var = IntVar()
    blue_checkbox = ttk.Checkbutton(main_frame, text="Blue", variable=blue_checkbox_var)
    blue_checkbox.grid(row=1, column=0, sticky=W)
    blue_checkbox['command'] = lambda: checkbox_event(organize_button, blue_checkbox_var.get(),
                                                      orange_checkbox_var.get())

    orange_checkbox_var = IntVar()
    orange_checkbox = ttk.Checkbutton(main_frame, text="Orange", variable=orange_checkbox_var)
    orange_checkbox.grid(row=2, column=0, sticky=W)
    orange_checkbox['command'] = lambda: checkbox_event(organize_button, blue_checkbox_var.get(),
                                                        orange_checkbox_var.get())

    organize_button = ttk.Button(main_frame, text="Organize", state=DISABLED)
    organize_button.grid(row=3, column=0)
    organize_button['command'] = lambda: send_pick_up(mqtt_client, blue_checkbox_var.get(), orange_checkbox_var.get())

    #     calibrate_arm_button = ttk.Button(main_frame, text="Calibrate Arm")
    #     calibrate_arm_button.grid(row=1, column=2)
    #     calibrate_arm_button['command'] = lambda: send_calibrate_arm(mqtt_client)

    pc_delegate = MyDelegateOnThePc(message_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


def send_check_area(mqtt_client):
    print("Asking ev3 if the room is clean")
    mqtt_client.send_message("check_area")


def send_pick_up(mqtt_client, blue, orange):
    print("Telling ev3 to clean room")
    mqtt_client.send_message("clean_room", [blue, orange])


def send_calibrate_arm(mqtt_client):
    print("Calibrating Arm")
    mqtt_client.send_message("calibrate_arm")


def checkbox_event(organize_button, blue_checkbox_state, orange_checkbox_state):
    if blue_checkbox_state == 1 or orange_checkbox_state == 1:
        organize_button.configure(state=NORMAL)
    else:
        organize_button.configure(state=DISABLED)


main()
