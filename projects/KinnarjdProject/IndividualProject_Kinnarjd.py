
import tkinter
from tkinter import ttk
import ev3dev.ev3 as ev3

import mqtt_remote_method_calls as com


def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to
    # receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    # DONE: 3. Implement the callbacks for the drive buttons. Set both the
    # click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.
    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())
    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_forward(mqtt_client,
                                                     int(left_speed_entry.get()),
                                                     int(right_speed_entry.get()))
    root.bind('<Up>', lambda event: send_forward(mqtt_client,
                                                 left_speed,
                                                 right_speed))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: send_left(mqtt_client,
                                               left_speed,
                                               right_speed)
    root.bind('<Left>', lambda event: send_left(mqtt_client,
                                                left_speed,
                                                right_speed))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: send_right(mqtt_client,
                                                 left_speed,
                                                 right_speed)
    root.bind('<Right>', lambda event: send_right(mqtt_client,
                                                  left_speed,
                                                  right_speed))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: send_back(mqtt_client,
                                               left_speed,
                                               right_speed)
    root.bind('<Down>', lambda event: send_back(mqtt_client,
                                                left_speed,
                                                right_speed))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# DONE: 4. Implement the functions for the drive button callbacks.
def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive forward")
    ev3.Sound.speak("Jonathan is Amazing").wait()
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


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
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
