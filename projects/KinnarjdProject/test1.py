#EV3
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.num = 0
        self.oldnum = 0

    def qright(self, num):
        ev3.Sound.speak("question {} correct".format(num)).wait()
        time.sleep(0.5)
        """Move the robot forward"""
        self.oldnum = self.num
        self.num = num + 1

    def qwrong(self, num):
        ev3.Sound.speak("question {} incorrect".format(num)).wait()
        time.sleep(0.5)
        """Move the robot backwards"""
        self.oldnum = self.num
        self.num = num + 1


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
    oldnum = 0
    while my_delegate.running:
        btn.process()
        if combo == 2 and btn.check_buttons(buttons=['up', 'right']):
            ev3.Sound.speak("You cracked the code, now answer the questions on the computer").wait()
            robot.arm_up()
            mqtt_client.send_message("cracked_the_code")
            robot.arm_down()
            combo = combo + 1
        elif combo == 0 and btn.check_buttons(buttons=['up', 'left']):
            ev3.Sound.speak("Correct Combo for the first part").wait()
            robot.arm_up()
            combo = combo + 1
        elif combo == 1 and btn.check_buttons(buttons=['down', 'right']):
            ev3.Sound.speak("Correct Combo for the second part, one left").wait()
            robot.arm_down()
            combo = combo + 1
        elif combo > 2 and my_delegate.num > oldnum:
            ev3.Sound.speak("Next").wait()
            mqtt_client.send_message("cracked_the_code")
            oldnum = my_delegate.num
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


"""def handle_questions():
    ev3.Sound.speak("Next").wait()
    time.sleep(0.5)
    new_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    mqtt_client.send_message("cracked_the_code")"""


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
