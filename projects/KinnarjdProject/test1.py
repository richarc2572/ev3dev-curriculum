#EV3
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = True

    def set_led(self, led_side_string, led_color_string):
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


def main():
    print("--------------------------------------------")
    print(" LED Button communication")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("Lego2").wait()
    # DONE: 3. Create an instance of your delegate class and an MQTT client,
    # passing in the delegate object.
    # Note: you can determine the variable names that you should use by looking at the errors underlined in later code.
    # Once you have that done connect the mqtt_client to the MQTT broker using the connect_to_pc method.
    # Note: on EV3 you call connect_to_pc, but in the PC code it will call connect_to_ev3
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    # Buttons on EV3 (these obviously assume TO DO: 3. is done)
    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Up")
    btn.on_down = lambda state: handle_button_press2(state, mqtt_client, "Down")
    btn.on_left = lambda state: handle_button_press3(state, mqtt_client, "Left")
    btn.on_right = lambda state: handle_button_press4(state, mqtt_client, "Right")
    btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)

    while my_delegate.running:
        btn.process()
        if btn.check_buttons(buttons=['up', 'left']):
            ev3.Sound.speak("Correct Combo").wait()
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
        # DONE: 4. Send a message using MQTT that will:
        #   -- Call the method called "button_pressed" on the delegate at the other end of the pipe.
        #   -- Pass the parameters [button_name] as a list.
        # This is meant to help you learn the mqtt_client.send_message syntax.
        # You can review the code above to understand how button_name is passed into this function.
        mqtt_client.send_message("incorrect_button_pressed", [button_name])


def handle_button_press2(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))

        # DONE: 4. Send a message using MQTT that will:
        #   -- Call the method called "button_pressed" on the delegate at the other end of the pipe.
        #   -- Pass the parameters [button_name] as a list.
        # This is meant to help you learn the mqtt_client.send_message syntax.
        # You can review the code above to understand how button_name is passed into this function.
        mqtt_client.send_message("correct_button_pressed", [button_name])


def handle_button_press3(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))

        # DONE: 4. Send a message using MQTT that will:
        #   -- Call the method called "button_pressed" on the delegate at the other end of the pipe.
        #   -- Pass the parameters [button_name] as a list.
        # This is meant to help you learn the mqtt_client.send_message syntax.
        # You can review the code above to understand how button_name is passed into this function.
        mqtt_client.send_message("correct_button_pressed", [button_name])


def handle_button_press4(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))

        # DONE: 4. Send a message using MQTT that will:
        #   -- Call the method called "button_pressed" on the delegate at the other end of the pipe.
        #   -- Pass the parameters [button_name] as a list.
        # This is meant to help you learn the mqtt_client.send_message syntax.
        # You can review the code above to understand how button_name is passed into this function.
        mqtt_client.send_message("correct_button_pressed", [button_name])


def handle_shutdown(button_state, my_delegate):
    """Exit the program."""
    if button_state:
        my_delegate.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
