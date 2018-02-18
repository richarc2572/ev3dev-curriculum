import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = False
        self.room_is_clean = True
        self.robot = robo.Snatch3r()
        self.mqtt_client = None

    def clean_room(self):
        if self.room_is_clean:
            print("Room is already clean")
            ev3.Sound.speak("Room is already clean")
        else:
            print("Cleaning room")
            ev3.Sound.speak("Cleaning room")
            self.room_is_clean = True

    def is_room_clean(self):
        self.mqtt_client.send_message("is_room_clean", [self.room_is_clean])

    def loop_forever(self):
        self.running = True
        btn = ev3.Button()
        self.robot.pixy.mode = "SIG1"
        while not btn.backspace and self.running:
            if self.robot.pixy.value(1) == 0:
                self.room_is_clean = True
            else:
                self.room_is_clean = False
            time.sleep(0.01)
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()


def main():
    ev3.Sound.speak("Room Cleaner").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    my_delegate.mqtt_client = mqtt_client
    my_delegate.loop_forever()


main()
