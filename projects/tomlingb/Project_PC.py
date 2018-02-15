import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):
    def command_response(self, response):
        print(response)


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)

    left_speed = 200
    right_speed = 200

    root = tkinter.Tk()
    root.title("Geoffrey's Dungeon")

    main_frame = ttk.Frame(root, padding=10, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame,
                      text='Command your champion from here')
    label.grid(columnspan=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed, right_speed)
    root.bind('w', lambda event: send_forward(mqtt_client, left_speed, right_speed))

    backward_button = ttk.Button(main_frame, text='Backward')
    backward_button.grid(row=3, column=1)
    backward_button['command'] = lambda: send_back(mqtt_client, left_speed, right_speed)
    root.bind('s', lambda event: send_back(mqtt_client, left_speed, right_speed))

    left_button = ttk.Button(main_frame, text='Left')
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_left(mqtt_client, left_speed, right_speed)
    root.bind('a', lambda event: send_left(mqtt_client, left_speed, right_speed))

    right_button = ttk.Button(main_frame, text='Right')
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_right(mqtt_client, left_speed, right_speed)
    root.bind('d', lambda event: send_right(mqtt_client, left_speed, right_speed))

    attack_button = ttk.Button(main_frame, text='Attack')
    attack_button.grid(row=4, column=1)
    attack_button['command'] = lambda: send_attack(mqtt_client)
    root.bind('p', lambda event: send_attack(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=0)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    e_button = ttk.Button(main_frame, text="Exit on EV3 too")
    e_button.grid(row=5, column=2)
    e_button['command'] = lambda: quit_program(mqtt_client, True)

    root.mainloop()


def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive forward")
    mqtt_client.send_message("forward", [left_speed_entry, right_speed_entry])


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("turn left")
    mqtt_client.send_message("turn_left", [left_speed_entry,
                                           right_speed_entry])


def send_stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("turn right")
    mqtt_client.send_message("turn_right", [left_speed_entry,
                                            right_speed_entry])


def send_back(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive backward")
    mqtt_client.send_message("backward", [left_speed_entry, right_speed_entry])


def send_attack(mqtt_client):
    print('attack')


def quit_program(mqtt_client, shutdown_ev3):
    print('exit')
    if shutdown_ev3:
        mqtt_client.send_message("exit")
    mqtt_client.close()
    exit()


main()
