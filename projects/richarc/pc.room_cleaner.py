import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):

    def __init__(self, room_status_label):
        self.room_status_label = room_status_label

    def is_room_clean(self, room_is_clean):
        if room_is_clean:
            self.room_status_label.configure(text="The room is clean.")
        else:
            self.room_status_label.configure(text="The room is dirty.")


def main():
    root = tkinter.Tk()
    root.title("Room Cleaner")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    message_label = ttk.Label(main_frame, text="--")
    message_label.grid(row=0, column=0)

    check_room_button = ttk.Button(main_frame, text="Check Room")
    check_room_button.grid(row=1, column=0)
    check_room_button['command'] = lambda: send_is_room_clean(mqtt_client)

    clean_button = ttk.Button(main_frame, text="Clean Room")
    clean_button.grid(row=1, column=1)
    clean_button['command'] = lambda: send_clean_room(mqtt_client)

    return_home_button = ttk.Button(main_frame, text="Go Home")
    return_home_button.grid(row=1, column=3)
    return_home_button['command'] = lambda: send_return_home(mqtt_client)

    calibrate_arm_button = ttk.Button(main_frame, text="Calibrate Arm")
    calibrate_arm_button.grid(row=1, column=2)
    calibrate_arm_button['command'] = lambda: send_calibrate_arm(mqtt_client)

    pc_delegate = MyDelegateOnThePc(message_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


def send_is_room_clean(mqtt_client):
    print("Asking ev3 if the room is clean")
    mqtt_client.send_message("is_room_clean")


def send_clean_room(mqtt_client):
    print("Telling ev3 to clean room")
    mqtt_client.send_message("clean_room")


def send_return_home(mqtt_client):
    print("Going Home")
    mqtt_client.send_message("return_home")


def send_calibrate_arm(mqtt_client):
    print("Calibrating Arm")
    mqtt_client.send_message("calibrate_arm")


main()
