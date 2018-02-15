#PC
"""
There are no TODOs in this module.  You will simply run this code on your PC to communicate with the EV3.  Feel free
to look at the code to see if you understand what is going on, but no changes are needed to this file.

See the m3_ev3_led_button_communication.py file for all the details.

Author: David Fisher.
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in
        self.questionNum = 0

    def incorrect_button_pressed(self, button_name):
        print("Incorrect Button: " + button_name)
        message_to_display = "{} was pressed, try more than one at a time".format(button_name)
        self.display_label.configure(text=message_to_display)

    def cracked_the_code(self):
        questions = ["Que 1", "Que 2", "Que 3", "Oue 4"]
        if self.questionNum < len(questions):
            # message_to_display = "question: {}".format(questions[self.questionNum])
            message_to_display = "Balls"
            self.display_label.configure(text=message_to_display)
            self.questionNum = self.questionNum + 1
        else:
            self.display_label.configure(text="We are all out of questions")
            self.questionNum = self.questionNum + 1


def main():
    questions = ["Que 1", "Que 2", "Que 3", "Oue 4"]
    root = tkinter.Tk()
    root.title("Crack the Code to Rob the Bank")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    button_message = ttk.Label(main_frame, text="--")

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_side_label = ttk.Label(main_frame, text="Choice Option 1")
    left_side_label.grid(row=0, column=0)

    left_green_button = ttk.Button(main_frame, text="Yes")
    left_green_button.grid(row=1, column=0)
    questionnumer = pc_delegate.questionNum
    left_green_button['command'] = lambda: send_choice(mqtt_client, "Yes", questionnumer)

    button_label = ttk.Label(main_frame, text="{}".format(questions[questionnumer]))
    button_label.grid(row=1, column=1)

    button_message.grid(row=2, column=1)

    right_side_label = ttk.Label(main_frame, text="Choice Option 2")
    right_side_label.grid(row=0, column=2)

    right_green_button = ttk.Button(main_frame, text="No")
    right_green_button.grid(row=1, column=2)
    right_green_button['command'] = lambda: send_choice(mqtt_client, "No", questionnumer)

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()

# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------


def send_choice(mqtt_client, answer, questionnum):
    print("Sending either move up or move back depending on the answer: ".format(answer))
    questionanswers = ["Yes", "No", "Yes", "No"]
    print(answer, questionnum, questionanswers[questionnum], answer == questionanswers[questionnum])
    if questionnum <= len(questionanswers):
        if answer == questionanswers[questionnum]:
            mqtt_client.send_message("qright", [questionnum])
        elif answer != questionanswers[questionnum]:
            mqtt_client.send_message("qwrong", [questionnum])
        else:
            print("It is not working")
    else:
        print("Too big of a question number index")


def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


main()
