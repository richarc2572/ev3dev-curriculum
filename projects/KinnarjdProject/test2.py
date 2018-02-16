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
        self.index = 0

    def incorrect_button_pressed(self, button_name):
        print("Incorrect Button: " + button_name)
        message_to_show = "{} was pressed, try more than one at a time".format(button_name)
        self.display_label.configure(text=message_to_show)

    def cracked_the_code(self):
        self.display_label.configure(text="answer the first question")

    def tester(self, labelwithstring):
        # change the delegate's label to have the given text
        self.display_label = labelwithstring
        # self.display_label.configure(text=string)
        # self.display_label["text"] = string
        print("try it out")

    def they_won(self):
        self.display_label["text"] = "you won the game!"
        winner_sequence()


index = 0


def main():
    root = tkinter.Tk()
    root.title("Crack the Code to Rob the Bank")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    button_label = ttk.Label(main_frame, text="Get Ready to Answer Questions")
    button_label.grid(row=1, column=1)
    pc_delegate = MyDelegateOnThePc(button_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    left_side_label = ttk.Label(main_frame, text="Choice Option 1")
    left_side_label.grid(row=0, column=0)

    left_green_button = ttk.Button(main_frame, text="Yes")
    left_green_button.grid(row=1, column=0)
    left_green_button['command'] = lambda: send_choice(mqtt_client, "Yes", pc_delegate, root, main_frame)
    # button_label = labeler(pc_delegate, main_frame)

    right_side_label = ttk.Label(main_frame, text="Choice Option 2")
    right_side_label.grid(row=0, column=2)

    right_green_button = ttk.Button(main_frame, text="No")
    right_green_button.grid(row=1, column=2)
    right_green_button['command'] = lambda: send_choice(mqtt_client, "No", pc_delegate, root, main_frame)

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


def send_choice(mqtt_client, answer, delegate, root, main_frame):
    print("Sending either move up or move back depending on the answer: ".format(answer))
    questions = ["Choose Dr. Mutchler as your getaway driver?",
                 "Did you copy the heist from the Ocean's 11??",
                 "Police chopper in the sky, do you keep going?",
                 "Does your mom know you are robbing a bank today?",
                 "Also did you wear an awesome real black leather coat?",
                 "Did you remember to use the bathroom before this heist?",
                 "The cops are on behind you, do you want to give up now??",
                 "Your tire just popped, do you stop at the mechanic right now?",
                 "You forgot to have breakfast, should you stop at Wendy's on the way??"]
    questionanswers = ["Yes", "No", "Yes", "No", "Yes", "Yes", "No", "No", "No"]
    root.title("Crack the Code to Rob")
    if delegate.index < len(questionanswers):
        button_label = ttk.Label(main_frame, text=questions[delegate.index])
        button_label.grid(row=1, column=1)
        delegate.tester(button_label)
        if answer == questionanswers[delegate.index]:
            mqtt_client.send_message("drive_unless_line", [delegate.index])
            delegate.index = delegate.index + 1
        elif answer != questionanswers[delegate.index]:
            mqtt_client.send_message("driveback_unless_line", [delegate.index])
            delegate.index = delegate.index + 1
        else:
            print("Something went wrong")
    else:
        button_label = ttk.Label(main_frame,
                                 text="I am sorry, but you are out of questions, "
                                      "this means you did not make it home in time!")
        button_label.grid(row=1, column=1)
        delegate.tester(button_label)
        print("Out of Questions, You loose if you have not gotten to the line by now")
        mqtt_client.send_message("indexout")


def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


def labeler(delegate, frame):
    questions = ["Did you choose Dr. Mutchler as your getaway driver?", "Did you copy the heist from Ocean's 11?",
                 "Does your mom know you are robbing a bank?", "Are you wearing a black leather jacket?"]
    return ttk.Label(frame, text=questions[delegate.index])


def winner_sequence():
    print("call on the robot to say congrats or something")


main()

