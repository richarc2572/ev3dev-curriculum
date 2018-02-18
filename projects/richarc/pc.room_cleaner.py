import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Room Cleaner")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    message_label = ttk.Label(main_frame, text="--")
    message_label.grid(row=0, column=0)

    clean_button = ttk.Button(main_frame, text="Clean Room")
    clean_button.grid(row=1, column=0)
    clean_button['command'] = lambda: send_clean_room(mqtt_client)

    root.mainloop()


def send_clean_room(mqtt_client):
    print("Telling ev3 to clean room")
    mqtt_client.send_message("clean_room")


main()
