import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = False

    def clean_room(self):
        print("Cleaning room")

    def loop_forever(self):
        self.running = True
        btn = ev3.Button()
        while not btn.backspace and self.running:
            time.sleep(0.01)
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()


def main():
    ev3.Sound.speak("Room Cleaner").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    my_delegate.loop_forever()


main()
