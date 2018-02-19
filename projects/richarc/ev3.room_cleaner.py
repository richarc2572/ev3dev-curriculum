import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = False
        self.robot = robo.Snatch3r()
        self.mqtt_client = None

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
                    if abs(dx) < 5:
                        self.robot.stop_fast()
                        self.robot.turn_degrees(-5, 100)
                        self.robot.arm_down()
                        self.robot.turn_degrees(25, 100)
                        self.robot.drive_inches(3, 100)
                        self.return_home()
                        self.robot.turn_degrees(90, 200)
                        self.robot.drive_inches(5, 200)
                        self.robot.arm_down()
                        self.robot.drive_inches(-5, 200)
                        self.robot.turn_degrees(-90, 200)
                        break
                    else:
                        self.robot.move(-2 * dx, 2 * dx)
                elif dwidth > 5 and x != 0:
                    if dx > 10:
                        self.robot.move(5 * dwidth, 10 * dwidth)
                    elif dx < -10:
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

    def is_room_clean(self):
        self.robot.pixy.mode = "SIG1"
        width1 = self.robot.pixy.value(3)
        self.robot.pixy.mode = "SIG2"
        width2 = self.robot.pixy.value(3)
        if width1 and width2 < 1:
            self.mqtt_client.send_message("is_room_clean", [True])
        else:
            self.mqtt_client.send_message("is_room_clean", [False])

    def return_home(self):
        self.robot.arm_up()
        btn = ev3.Button()
        self.robot.pixy.mode = "SIG3"
        while not btn.backspace and self.robot.color_sensor.reflected_light_intensity > 10:
            x = self.robot.pixy.value(1)
            width = self.robot.pixy.value(3)
            dx = 135 - x
            dwidth = 50 - width
            if width > 5:
                if width > 35:
                    self.robot.move(-200, -200)
                else:
                    if dx > 5:
                        self.robot.move(2.5 * dx, 5 * dx)
                    elif dx < -5:
                        print(dx)
                        self.robot.move(-5 * dx, -2.5 * dx)
                    else:
                        self.robot.move(5 * dwidth, 5 * dwidth)
            else:
                self.robot.move(200, -200)
            time.sleep(0.1)
        while not btn.backspace:
            x = self.robot.pixy.value(1)
            dx = 135 - x
            if dx > 5:
                self.robot.move(-100, 100)
            elif dx < -5:
                self.robot.move(100, -100)
            else:
                while self.robot.color_sensor.reflected_light_intensity < 10:
                    self.robot.move(100, 100)
                    time.sleep(0.1)
                break
            time.sleep(0.1)
        self.robot.turn_degrees(180, 200)
        self.robot.stop()

    def calibrate_arm(self):
        self.robot.arm_calibration()

    def loop_forever(self):
        self.running = True
        btn = ev3.Button()
        self.robot.pixy.mode = "SIG1"
        while not btn.backspace and self.running:
            time.sleep(0.01)
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()


def main():
    #     ev3.Sound.speak("Room Cleaner").wait()
    print("Ready")
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    my_delegate.mqtt_client = mqtt_client
    my_delegate.loop_forever()


main()
