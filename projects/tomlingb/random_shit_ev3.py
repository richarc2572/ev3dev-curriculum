#!/usr/bin/env python3

import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time
import random


class MyDelegate(object):
    def __init__(self):
        self.running = True
        self.lost = False
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.left_speed = 200
        self.right_speed = 200
        self.color = 0
        self.turn = 2
        self.available_colors = [0, 1, 2, 3, 4, 5, 6]
        self.spoken_colors = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        self.color_list = []
        self.active_list = False
        self.guess_list = []
        self.color_number = 0
        self.send_count = 0
        self.sensor = ev3.ColorSensor()
        assert self.sensor

    def move_direction(self, direction_string):
        print("Receiving: {}".format(direction_string))

        if direction_string == "forward":
            self.left_motor.run_forever(speed_sp=self.left_speed)
            self.right_motor.run_forever(speed_sp=self.right_speed)
        elif direction_string == "backward":
            self.left_motor.run_forever(speed_sp=-self.left_speed)
            self.right_motor.run_forever(speed_sp=-self.right_speed)
        elif direction_string == "turn_right":
            self.left_motor.run_forever(speed_sp=self.left_speed)
            self.right_motor.run_forever(speed_sp=-self.right_speed)
        elif direction_string == "turn_left":
            self.left_motor.run_forever(speed_sp=-self.left_speed)
            self.right_motor.run_forever(speed_sp=self.right_speed)
        elif direction_string == "stop":
            self.left_motor.stop()
            self.right_motor.stop()

    def check_color(self):
        if self.sensor.color == ev3.ColorSensor.COLOR_RED:
            print('red')
            self.color = ev3.ColorSensor.COLOR_RED
        elif self.sensor.color == ev3.ColorSensor.COLOR_BLUE:
            print('blue')
            self.color = ev3.ColorSensor.COLOR_BLUE
        elif self.sensor.color == ev3.ColorSensor.COLOR_GREEN:
            print('green')
            self.color = ev3.ColorSensor.COLOR_GREEN
        elif self.sensor.color == ev3.ColorSensor.COLOR_YELLOW:
            print('yellow')
            self.color = ev3.ColorSensor.COLOR_YELLOW

    def next_turn(self):
        self.turn += 1
        self.active_list = False
        self.guess_list = []

    def create_color_list(self):
        if self.active_list is False:
            self.color_list = []
            for k in range(self.turn):
                self.color_number = random.randint(2, 5)
                self.color_list.append(self.available_colors[self.color_number])
                time.sleep(0.5)
                ev3.Sound.speak(self.spoken_colors[self.color_number]).wait()
            print('Color List', self.color_list)
            print('Blue', ev3.ColorSensor.COLOR_BLUE)
        self.active_list = True

    def guess(self):
        count = 0
        ev3.Sound.beep().wait()
        self.send_count = 0
        if self.sensor.color == ev3.ColorSensor.COLOR_RED:
            print('red')
            self.color = ev3.ColorSensor.COLOR_RED
        elif self.sensor.color == ev3.ColorSensor.COLOR_BLUE:
            print('blue')
            self.color = ev3.ColorSensor.COLOR_BLUE
        elif self.sensor.color == ev3.ColorSensor.COLOR_GREEN:
            print('green')
            self.color = ev3.ColorSensor.COLOR_GREEN
        elif self.sensor.color == ev3.ColorSensor.COLOR_YELLOW:
            print('yellow')
            self.color = ev3.ColorSensor.COLOR_YELLOW

        self.guess_list.append(self.available_colors[self.color])
        print('guess list', self.guess_list)
        if len(self.color_list) != 0:
            for k in range(len(self.guess_list)):
                if self.guess_list[k] == self.color_list[k]:
                    count += 1
            if count != len(self.guess_list):
                self.lost = True
            if self.guess_list == self.color_list:
                print('You Win!!')
                ev3.Sound.speak('Correct!').wait()
                self.color_list = []
        else:
            ev3.Sound.speak('Press Next to start the next round').wait()
        print('count:', count)

    def shutdown(self):
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.running = False
        print('Goodbye!')
        ev3.Sound.speak("Goodbye").wait()


def main():
    print("--------------------------------------------")
    print(" Memory Game")
    print("--------------------------------------------")
    ev3.Sound.speak("Starting").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    while my_delegate.running and my_delegate.lost is False:
        my_delegate.create_color_list()
        if my_delegate.color != 0:
            send_color(mqtt_client, my_delegate.color)
            my_delegate.send_count += 1
        time.sleep(0.01)

    if my_delegate.lost is True:
        ev3.Sound.speak("You Lost").wait()

    my_delegate.shutdown()


def send_color(mqtt_client, color):
    mqtt_client.send_message("color_submitted", [color])


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
