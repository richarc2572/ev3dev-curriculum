import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = False
        self.room_is_clean = False
        self.robot = robo.Snatch3r()
        self.mqtt_client = None

    def clean_room(self):
        self.robot.pixy.mode = "SIG1"
        if self.room_is_clean:
            print("Room is already clean")
            ev3.Sound.speak("Room is already clean").wait()
        else:
            btn = ev3.Button()
            print("Cleaning room")
            ev3.Sound.speak("Cleaning room").wait()

            self.robot.arm_up()
            while not btn.backspace:
                x = self.robot.pixy.value(1)
                width = self.robot.pixy.value(3)
                dx = 125 - x
                dwidth = 58 - width
                print(x, width, dx, dwidth)
                if abs(dwidth) < 5:
                    if abs(dx) < 5:
                        self.robot.stop_fast()
                        self.robot.turn_degrees(-5, 100)
                        self.robot.arm_down()
                        self.robot.turn_degrees(23, 100)
                        self.robot.drive_inches(2.75, 100)
                        self.robot.arm_position(5)
                        self.robot.turn_degrees(90, 100)
                        self.robot.arm_down()
                        self.robot.drive_inches(-3, 100)
                        self.robot.turn_degrees(-90, 100)
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

    def is_room_clean(self):
        self.mqtt_client.send_message("is_room_clean", [self.room_is_clean])

    def calibrate_arm(self):
        self.robot.arm_calibration()

    def loop_forever(self):
        self.running = True
        btn = ev3.Button()
        self.robot.pixy.mode = "SIG1"
        while not btn.backspace and self.running:
            # if self.robot.pixy.value(1) == 0:
            #     self.room_is_clean = True
            # else:
            #     self.room_is_clean = False
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
