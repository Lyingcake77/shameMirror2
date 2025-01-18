#import RPi.LGPIO as GPIO
from gpiozero import LED, RotaryEncoder, Button
from time import sleep
import subprocess
def start():
    red = LED(16)
    encoder = RotaryEncoder(a=17, b=27, wrap=True, max_steps=25)
    # Initialize the rotary encoder's SW pin on GPIO pin 22
    button = Button(22)
    last_rotary_value = 0
    ledOn = False
    try:
        while True:  # Infinite loop to continuously monitor the encoder
            current_rotary_value = encoder.steps  # Read current step count from rotary encoder

            # Check if the rotary encoder value has changed
            if last_rotary_value != current_rotary_value:
                print("Result =", current_rotary_value)  # Print the current value
                last_rotary_value = current_rotary_value  # Update the last value
                command = ["amixer", "sset", "Master", "{}%".format(current_rotary_value*4)]
                subprocess.Popen(command)

            # Check if the rotary encoder is pressed
            if button.is_pressed:
                print("Button pressed!")  # Print message on button press
                button.wait_for_release()  # Wait until button is released
                if ledOn == False:
                    red.on()
                else:
                    red.off()
                ledOn = not ledOn

            sleep(0.1)  # Short delay to prevent excessive CPU usage

    except KeyboardInterrupt:
        print("Program terminated")  # Print message when program is terminated via keyboard interrupt

    '''
    volume = 0
    while True:
        if volume > 100:
            volume = 0
        command = ["amixer", "sset", "Master", "{}%".format(volume)]
        subprocess.Popen(command)
        red.on()
        sleep(1)
        red.off()
        sleep(1)
        volume += 10
    '''