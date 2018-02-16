import ev3dev.ev3 as ev3
import time
import random
from PIL import Image
import mqtt_remote_method_calls as com
import robot_controller as robo

'''
class GameMaster(object):
    """ Delegate that listens for responses from EV3. """

    def __init__(self):
        self.mqtt_client = None
        self.running = False
        self.current_direction = 0
        self.robot = robo.Snatch3r

    def loop_forever(self):
        btn = ev3.Button()
        self.running = True
        while not btn.backspace and self.running:
            # Do nothing while waiting for commands
            time.sleep(0.01)
        self.mqtt_client.close()
        # Copied from robot.shutdown
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

    def exit(self):
        self.running = False
        
    def forwar(self, left_speed, right_speed):
        self.robot.forward(self, left_speed, right_speed)

    def backward(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def turn_left(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def turn_right(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)



    def randomly_display_new_dice(self):
        self.dice_values = [0, 0, 0, 0, 0]
        for i in range(self.num_active_dice):
            self.dice_values[i] = random.randrange(1, self.max_die_value + 1)
        self.update_lcd()

    def update_lcd(self):
        self.lcd.image.paste(self.dice_images[self.dice_values[0]], (5, 8))
        self.lcd.image.paste(self.dice_images[self.dice_values[1]], (62, 8))
        self.lcd.image.paste(self.dice_images[self.dice_values[2]], (119, 8))
        self.lcd.image.paste(self.dice_images[self.dice_values[3]], (33, 66))
        self.lcd.image.paste(self.dice_images[self.dice_values[4]], (91, 66))
        self.lcd.update()

    def loop_forever(self):
        btn = ev3.Button()
        self.running = True
        while not btn.backspace and self.running:
            # Do nothing while waiting for commands
            time.sleep(0.01)
        self.mqtt_client.close()
        # Copied from robot.shutdown
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

    def guess(self, number_guessed):
        correct_answer = 0
        for value in self.dice_values:
            if value % 2:
                correct_answer += value - 1
                # Even numbers have no stem (dot) in the middle and therefore are not roses.
                # The number 1 has a stem but no "petals" (dots) around it. Value 0
                # The number 3 has a stem and 2 "petals" (dots) around it. Value 2
                # The number 5 has a stem and 4 "petals" (dots) around it. Value 4
                # etc
                
                
        if number_guessed == correct_answer:
            print("{} is correct".format(correct_answer))
            if self.num_active_dice == 5:
                self.consecutive_correct += 1
                if self.consecutive_correct >= 3:
                    print("The player has won the game!")
                    self.mqtt_client.send_message("guess_response",
                                                  [
                                                      "{} is correct! You have won the game!!!!!!!!!!!!!!!!!!".format(
                                                          number_guessed)])
                    ev3.Sound.speak("Correct. You win!").wait()
                    ev3.Sound.play(
                        "/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()
                    print(
                        "Great work! Now let's make the game a bit harder. :)")
                    self.mqtt_client.send_message("guess_response", [
                        "You are done! You can get your checkoff!"])
                    self.mqtt_client.send_message("guess_response", [
                        "Optional: You can now play with more dots. :)"])
                    self.max_die_value = 9  # Make the game a little harder now.
                    self.consecutive_correct = 0
                else:
                    self.mqtt_client.send_message("guess_response",
                                                  [
                                                      "{} is correct! You have {} correct in a row.".format(
                                                          number_guessed,
                                                          self.consecutive_correct)])
                    ev3.Sound.speak("correct")
            else:
                self.consecutive_correct = 0
                self.mqtt_client.send_message("guess_response",
                                              [
                                                  "{} is correct! To win you need 3 wins WITH 5 DICE!".format(
                                                      number_guessed)])
                ev3.Sound.speak(
                    "Correct, but only {} dice.".format(self.num_active_dice))
        else:
            too_high_or_too_low = "Too high" if number_guessed > correct_answer else "Too low"
            self.mqtt_client.send_message("guess_response",
                                          [
                                              "Your guess of {} was {}. The correct answer for {} is {}".format(
                                                  number_guessed,
                                                  too_high_or_too_low,
                                                  self.dice_values,
                                                  correct_answer)])
            self.consecutive_correct = 0
            ev3.Sound.speak(too_high_or_too_low)
            print(too_high_or_too_low)
        self.randomly_display_new_dice()'''

'''
def main():
    print('ready')
    my_delegate = GameMaster()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    print("Welcome to the dungeon")
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus use EV3 as broker.
    my_delegate.loop_forever()


direction_dict = ['forward', 'backward', 'left', 'right']

'''


def main():
    ev3.Sound.speak("Hello").wait()
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
