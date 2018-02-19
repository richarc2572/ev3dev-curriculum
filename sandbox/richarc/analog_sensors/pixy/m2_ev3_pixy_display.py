#!/usr/bin/env python3
"""
The goal of this module is to practice using the Pixy and MQTT at the same time.  This module will send data from the
EV3 to the PC.

Authors: David Fisher and Clayton Richards.  February 2017.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    print("--------------------------------------------")
    print(" Pixy display")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Pixy display").wait()
    print("Press the touch sensor to exit this program.")

    # DONE: 2. Create an MqttClient (no delegate needed since EV3 will only send data, so an empty constructor is fine)
    # Then connect to the pc using the connect_to_pc method.
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_pc()

    robot = robo.Snatch3r()

    btn = ev3.Button()

    while not btn.backspace:
        # DONE: 3. Read the Pixy values for x, y, width, and height
        # Print the values (much like the print_pixy_readings example)
        robot.pixy.mode = "SIG3"
        x1 = robot.pixy.value(1)
        y1 = robot.pixy.value(2)
        width1 = robot.pixy.value(3)
        height1 = robot.pixy.value(4)

        robot.pixy.mode = "SIG4"
        x2 = robot.pixy.value(1)
        y2 = robot.pixy.value(2)
        width2 = robot.pixy.value(3)
        height2 = robot.pixy.value(4)

        print("(X, Y)=({}, {}) Width={} Height={}".format(x1, y1, width1, height1), end="")
        print("(X, Y)=({}, {}) Width={} Height={}".format(x2, y2, width2, height2))

        # DONE: 4. Send the Pixy values to the PC by calling the on_rectangle_update method
        # If you open m2_pc_pixy_display you can see the parameters for that method [x, y, width, height]
        mqtt_client.send_message("on_rectangle_update", [x1, y1, width1, height1, x2, y2, width2, height2])
        time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    mqtt_client.close()


# TODO: 5. Call over a TA or instructor to sign your team's checkoff sheet.
#
# Observations you should make, if the EV3 has data the PC can know that data too using MQTT.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
