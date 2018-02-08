import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    root = tkinter.Tk()
    root.title("Petals on a Rose")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame,
                      text='Please enter a command')
    label.grid(columnspan=2)

    direction = ttk.Entry(main_frame, width=8)
    direction.grid(row=2, column=0)

    command_button = ttk.Button(main_frame, text="Enter")
    command_button.grid(row=2, column=1)
    command_button['command'] = lambda: direction(mqtt_client, guess_entry)
    root.bind('<Return>', lambda event: direction(mqtt_client, guess_entry))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=3, column=0)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    e_button = ttk.Button(main_frame, text="Exit on EV3 too")
    e_button.grid(row=3, column=1)
    e_button['command'] = lambda: quit_program(mqtt_client, True)

    root.mainloop()


def direction():
