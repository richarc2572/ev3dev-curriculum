import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):
    def command_response(self, response):
        print(response)


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Geoffrey's Dungeon")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame,
                      text='Run your champion from here')
    label.grid(columnspan=2)

    command_entry = ttk.Entry(main_frame, width=15)
    command_entry.grid(row=2, column=0)

    command_button = ttk.Button(main_frame, text="Enter")
    command_button.grid(row=2, column=1)
    command_button['command'] = lambda: command(mqtt_client, command_entry)
    root.bind('<Return>', lambda event: command(mqtt_client, command_entry))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=3, column=0)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    e_button = ttk.Button(main_frame, text="Exit on EV3 too")
    e_button.grid(row=3, column=1)
    e_button['command'] = lambda: quit_program(mqtt_client, True)

    root.mainloop()


def command(mqtt_client, command_entry):
    mqtt_client.send_message("command", [command_entry.get().split()])
    command_entry.delete(0, 'end')


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        mqtt_client.send_message("exit")
    mqtt_client.close()
    exit()


main()
