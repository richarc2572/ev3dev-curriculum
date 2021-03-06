"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time
import mqtt_remote_method_calls as com


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.running = None
        assert self.arm_motor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.touch_sensor
        assert self.color_sensor
        assert self.ir_sensor
        assert self.pixy

        self.MAX_SPEED = 900

    def drive_inches(self, inches_target, speed_deg_per_second):
        assert self.left_motor.connected
        assert self.right_motor.connected
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_target * degrees_per_inch
        position_sp = motor_turns_needed_in_degrees
        self.left_motor.run_to_rel_pos(position_sp=position_sp,
                                       speed_sp=speed_deg_per_second,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=position_sp,
                                        speed_sp=speed_deg_per_second,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        assert self.left_motor.connected
        assert self.right_motor.connected
        motor_turn = degrees_to_turn * 4.45
        self.left_motor.run_to_rel_pos(position_sp=-motor_turn,
                                       speed_sp=turn_speed_sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=motor_turn,
                                        speed_sp=turn_speed_sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
        self.arm_motor.stop()
        ev3.Sound.beep().wait()
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0

    def arm_position(self, revolutions):
        if revolutions < 14.2:
            self.arm_motor.run_to_abs_pos(position_sp=360 * revolutions, speed_sp=self.MAX_SPEED)
            self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
        self.arm_motor.stop()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def shutdown(self):
        self.arm_motor.stop()
        self.left_motor.stop()
        self.right_motor.stop()
        self.running = False
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye!')
        ev3.Sound.speak("Goodbye").wait()

    def drive_unless_line(self, num):
        """Created by Jonathan Kinnard"""
        """This drives forward for two seconds unless it hits a black line"""
        ev3.Sound.speak("question {} correct".format(num)).wait()
        for k in range(50):
            if self.color_sensor.color != 1:
                self.move(600, 600)
            else:
                self.stop()
                mqtt_client = com.MqttClient()
                mqtt_client.connect_to_pc()
                mqtt_client.send_message("they_won")
                ev3.Sound.speak("You won the game well done").wait()
                break
            time.sleep(0.01)
        self.stop_fast()
        ev3.Sound.beep().wait()

    def driveback_unless_line(self, num):
        """Created by Jonathan Kinnard"""
        """This drives forward for two seconds unless it hits a black line"""
        ev3.Sound.speak("question {} incorrect".format(num)).wait()
        for k in range(50):
            self.backward(600, 600)
            time.sleep(0.01)
        self.stop()
        ev3.Sound.beep().wait()

    def move(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def backward(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def turn_left(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def turn_right(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def stop_fast(self):
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def seek_beacon(self):
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.move(-100, 100)
                time.sleep(1)
            else:
                if math.fabs(current_heading) < 1.5:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance <= 1:
                        self.drive_inches(2, 200)
                        self.stop()
                        return True
                    else:
                        self.move(300, 300)
                elif math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.move(-100, 100)
                    else:
                        self.move(100, -100)
                else:
                    print("Heading to far off")
                    self.move(-100, 100)
                    time.sleep(1)
            time.sleep(0.2)
        print("Abandon ship!")
        self.stop()
        return False

    def pick_up(self, color):
        if not self.touch_sensor.is_pressed:
            self.arm_up()
        btn = ev3.Button()
        self.pixy.mode = color
        while not btn.backspace:
            x = self.pixy.value(1)
            width = self.pixy.value(3)
            dx = 125 - x
            dwidth = 62 - width
            if abs(dwidth) < 5:
                if abs(dx) < 8:
                    self.stop_fast()
                    self.turn_degrees(-10, 200)
                    self.arm_down()
                    self.turn_degrees(30, 200)
                    self.drive_inches(2.5, 200)
                    self.arm_up()
                    break
                else:
                    self.move(-2 * dx, 2 * dx)
            elif dwidth > 5 and x != 0:
                if dx > 5:
                    self.move(5 * dwidth, 10 * dwidth)
                elif dx < -5:
                    self.move(10 * dwidth, 5 * dwidth)
                else:
                    self.move(10 * dwidth, 10 * dwidth)
            elif dwidth < -5 and x != 0:
                self.move(-200, -200)
            else:
                self.move(200, -200)
            time.sleep(0.1)
        self.stop()

    def take_home(self, color):
        if not self.touch_sensor.is_pressed:
            self.arm_up()
        self.turn_degrees(180, 200)
        btn = ev3.Button()
        self.pixy.mode = color
        while not btn.backspace:
            x = self.pixy.value(1)
            width = self.pixy.value(3)
            dx = 125 - x
            dwidth = 130 - width
            if abs(dx) < 10:
                if abs(dwidth) < 5:
                    self.turn_degrees(25, 200)
                    self.drive_inches(1, 200)
                    self.arm_down()
                    self.drive_inches(-3, 200)
                    break
                elif dwidth < -5:
                    self.move(-200, -200)
                elif dx > 5:
                    self.move(300 + 2 * dx, 300 + 5 * dx)
                elif dx < -5:
                    self.move(300 - 5 * dx, 300 - 2 * dx)
                else:
                    self.move(200 + 2 * dwidth, 200 + 2 * dwidth)
            elif abs(dx) >= 10:
                self.move(-3 * dx, 3 * dx)
            else:
                self.move(-200, 200)
            time.sleep(0.1)
        self.stop()
        if color == "SIG1":
            self.turn_degrees(-90, 200)
            self.drive_inches(10, 200)
            self.turn_degrees(-90, 200)
            self.drive_inches(-5, 200)
        else:
            self.turn_degrees(100, 200)
            self.drive_inches(10, 200)
            self.turn_degrees(100, 200)
        ev3.Sound.beep()
