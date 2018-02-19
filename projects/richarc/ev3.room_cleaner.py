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

    def clean_room(self):
        self.robot.arm_up()
        self.robot.pixy.mode = "SIG1"
        width1 = self.robot.pixy.value(3)
        self.robot.pixy.mode = "SIG2"
        width2 = self.robot.pixy.value(3)
        if width1 and width2 < 1:
            print("Room is already clean")
        #             ev3.Sound.speak("Room is already clean").wait()
        else:
            btn = ev3.Button()
            print("Cleaning room")
            #             ev3.Sound.speak("Cleaning room").wait()
            while not btn.backspace:
                if width2 > width1:
                    x = self.robot.pixy.value(1)
                    width = self.robot.pixy.value(3)
                else:
                    self.robot.pixy.mode = "SIG1"
                    x = self.robot.pixy.value(1)
                    width = self.robot.pixy.value(3)
                dx = 125 - x
                dwidth = 60 - width
                if abs(dwidth) < 5:
                    if abs(dx) < 6:
                        self.robot.stop_fast()
                        self.robot.turn_degrees(-5, 200)
                        self.robot.arm_down()
                        self.robot.turn_degrees(24, 200)
                        self.robot.drive_inches(3, 200)
                        # self.return_home()
                        # self.robot.turn_degrees(90, 200)
                        # self.robot.drive_inches(5, 200)
                        # self.robot.arm_down()
                        # self.robot.drive_inches(-5, 200)
                        # self.robot.turn_degrees(-90, 200)
                        break
                    else:
                        self.robot.move(-2 * dx, 2 * dx)
                elif dwidth > 5 and x != 0:
                    if dx > 5:
                        self.robot.move(5 * dwidth, 10 * dwidth)
                    elif dx < -5:
                        self.robot.move(10 * dwidth, 5 * dwidth)
                    else:
                        self.robot.move(10 * dwidth, 10 * dwidth)
                elif dwidth < -5 and x != 0:
                    self.robot.move(-200, -200)
                else:
                    self.robot.move(200, -200)
                time.sleep(0.1)
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

    def return_home(self):
        self.robot.arm_up()
        self.robot.pixy.mode = "SIG2"
        while self.robot.color_sensor.color != 5:
            x = self.robot.pixy.value(1)
            dx = 150 - x
            if x == 0:
                self.robot.move(-200, 200)
            elif dx > 5:
                self.robot.move(5 * dx, 10 * dx)
            elif dx < -5:
                self.robot.move(-10 * dx, -5 * dx)
            else:
                self.robot.move(400, 400)
            time.sleep(0.1)
        self.robot.stop()
        self.robot.arm_down()
        self.robot.drive_inches(-5, 200)
        self.robot.turn_degrees(180, 200)

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
