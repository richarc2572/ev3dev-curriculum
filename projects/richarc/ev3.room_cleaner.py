import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = False
        self.robot = robo.Snatch3r()
        self.mqtt_client = None
        self.blue_position = 'Missing'
        self.orange_position = 'Missing'

    def organize(self, blue_option, orange_option):
        if blue_option == 1 and orange_option == 0:
            self.robot.pick_up("SIG1")
            self.robot.take_home("SIG1")
            self.blue_position = 'Home'
        elif blue_option == 0 and orange_option == 1:
            self.robot.pick_up("SIG2")
            self.robot.take_home("SIG2")
            self.orange_position = 'Home'
        else:
            self.robot.pixy.mode = "SIG1"
            width1 = self.robot.pixy.value(3)
            self.robot.pixy.mode = "SIG2"
            width2 = self.robot.pixy.value(3)
            if width1 > width2:
                self.robot.pick_up("SIG1")
                self.robot.take_home("SIG1")
                self.blue_position = 'Home'
                self.robot.pick_up("SIG2")
                self.robot.take_home("SIG2")
                self.orange_position = 'Home'
            else:
                self.robot.pick_up("SIG2")
                self.robot.take_home("SIG2")
                self.orange_position = 'Home'
                self.robot.pick_up("SIG1")
                self.robot.take_home("SIG1")
                self.blue_position = 'Home'
        self.robot.stop()
        self.robot.arm_down()

    def check_area(self):
        if not self.robot.touch_sensor.is_pressed:
            self.robot.arm_up()

        self.robot.pixy.mode = "SIG1"
        width = self.robot.pixy.value(3)
        if width > 10:
            self.blue_position = 'Found'
        else:
            self.blue_position = 'Missing'

        self.robot.pixy.mode = "SIG2"
        width = self.robot.pixy.value(3)
        if width > 10:
            self.orange_position = 'Found'
        else:
            self.orange_position = 'Missing'

        self.mqtt_client.send_message("message_from_ev3", [self.blue_position, self.orange_position])

    def take_home(self, color):
        self.robot.take_home(color)

    def calibrate_arm(self):
        self.robot.arm_calibration()

    def loop_forever(self):
        self.running = True
        btn = ev3.Button()
        self.robot.pixy.mode = "SIG1"
        while not btn.backspace and self.running:
            time.sleep(0.01)
        self.robot.shutdown()


def main():
    #     ev3.Sound.speak("Room Cleaner").wait()
    print("Ready")
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    my_delegate.mqtt_client = mqtt_client
    my_delegate.loop_forever()


main()
