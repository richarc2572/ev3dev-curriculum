#EV3
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.questionNum = 1

    def led_command(self, led_side_string, led_color_string):
        print("Received: {} {}".format(led_side_string, led_color_string))

        led_side = None
        if led_side_string == "left":
            led_side = ev3.Leds.LEFT
        elif led_side_string == "right":
            led_side = ev3.Leds.RIGHT

        led_color = None
        if led_color_string == "green":
            led_color = ev3.Leds.GREEN
        elif led_color_string == "red":
            led_color = ev3.Leds.RED
        elif led_color_string == "black":
            led_color = ev3.Leds.BLACK

        if led_side is None or led_color is None:
            print(
                "Invalid parameters sent to set_led. led_side_string = {} led_color_string = {}".format(
                    led_side_string, led_color_string))
        else:
            ev3.Leds.set_color(led_side, led_color)

    def q1right(self):
        ev3.Sound.speak("question {} correct".format(self.questionNum)).wait()
        self.questionNum = self.questionNum + 1
        """Move the robot forward"""
        handle_questions()

    def q1wrong(self):
        ev3.Sound.speak("question {} incorrect".format(self.questionNum)).wait()
        self.questionNum = self.questionNum + 1
        """Move the robot backwards"""
        handle_questions()


def main():
    print("--------------------------------------------")
    print(" LED Button communication")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("Bank Robber").wait()
    robot = robo.Snatch3r()
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    # Buttons on EV3 (these obviously assume TO DO: 3. is done)
    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Up")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "Down")
    btn.on_left = lambda state: handle_button_press(state, mqtt_client, "Left")
    btn.on_right = lambda state: handle_button_press(state, mqtt_client, "Right")
    btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)
    combo = 0
    while my_delegate.running:
        btn.process()
        if combo == 2 and btn.check_buttons(buttons=['up', 'right']):
            ev3.Sound.speak("You cracked the code, now answer the questions on the computer").wait()
            robot.arm_up()
            mqtt_client.send_message("cracked_the_code")
            robot.arm_down()
        elif combo == 0 and btn.check_buttons(buttons=['up', 'left']):
            ev3.Sound.speak("Correct Combo for the first part").wait()
            robot.arm_up()
            combo = combo + 1
        elif combo == 1 and btn.check_buttons(buttons=['down', 'right']):
            ev3.Sound.speak("Correct Combo for the second part, one left").wait()
            robot.arm_down()
            combo = combo + 1
        time.sleep(0.01)
    ev3.Sound.speak("Goodbye").wait()
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)


# ----------------------------------------------------------------------
# Button event callback functions
# ----------------------------------------------------------------------
def handle_button_press(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message("incorrect_button_pressed", [button_name])


def handle_shutdown(button_state, my_delegate):
    """Exit the program."""
    if button_state:
        my_delegate.running = False


def handle_questions():
    ev3.Sound.speak("Next Question").wait()
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    mqtt_client.send_message("cracked_the_code")


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
