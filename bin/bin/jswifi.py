#!/usr/bin/env python3
"""
Contains functions regarding the GPIO on the RPI.
See below for PIN layout.

#################################################
#                   Pin number                  #
#                   +---------+                 #
#        +3V3      |1         2|         +5V    #
# BCM_02           |3         4|         +5V    #
# BCM_03           |5         6|         GND    #
# BCM_04           |7         8|  BCM_14 / TX   #
#        GND       |9        10|  BCM_15 / RX   #
# BCM_17           |11       12|  BCM_18 / PWM0 #
# BCM_21    / 27   |13       14|         GND    #
# BCM_22           |15       16|  BCM_23        #
#        +3V3      |17       18|  BCM_24        #
# BCM_10    / SPI  |19       20|         GND    #
# BCM_09    / SPI  |21       22|  BCM_25        #
# BCM_11    / SPI  |23       24|  BCM_08 / SPI  #
#        GND       |25       26|  BCM_07 / SPI  #
#                   +---------+                 #
#################################################
"""
################################################################################
## Imports
import RPi.GPIO as GPIO #@UnresolvedImport
import time
import subprocess
import logging
import sys

LOG_FORMAT = '[%(asctime)-8s][%(levelname)s]:\t%(message)s'
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)

################################################################################
## Private variables
__PIN__RED   = 3
__PIN__GREEN = 5
__PIN__BLUE  = 7

__PIN__BUTTON1  = 16
__PIN__BUTTON2  = 18

__TIME_1MS = 1.0 / 1000.0

################################################################################
## Function declarations
def initialize():
    """
    initialize()

    Input:
        None
    
    Output:
        None
    
    Description:
        Set up three output pins to be used as the RGB code.
        Set up two input pins to e used as buttons.
        Using GPIO.BOARD instead of GPIO.BCM as an init mode, allows us to 
        refer to pin numbers (as in the inside of the diagram rectangle) instead
        of their BCM number (as in outside of the diagram rectangle).
    """
    ## Input / Outputs Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False )
    GPIO.setup(__PIN__RED,   GPIO.OUT)
    GPIO.setup(__PIN__GREEN, GPIO.OUT)
    GPIO.setup(__PIN__BLUE,  GPIO.OUT)
    GPIO.setup(__PIN__BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(__PIN__BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def read_pin_value(pin):
    """
    read_pin_value()

    Input:
        pin     -       An integer corresponding to the pin number of the input
                        to be read.  Refer to the diagram at the beginnig of
                        this file to determine which pins can be used.
    
    Output:
        feedback    -   A boolean value where False means the button has not
                        been pressed and True means the button was pressed.
                        
    
    Description:
                        Read the value of a pin that has been previously set up
                        as input (GPIO.IN)
    """
    feedback = GPIO.input(pin)
    return feedback


def set_led_color(my_color):
    """
    set_led_color()

    Input:
        my_color    -   
    
    Output:
        None
    
    Description:
                        Read the value of a pin that has been previously set up
                        as input (GPIO.IN)
    """
    if (my_color.lower() == "black" or my_color.lower() == "off"):
        GPIO.output(__PIN__RED,   False)
        GPIO.output(__PIN__GREEN, False)
        GPIO.output(__PIN__BLUE,  False)

    elif (my_color.lower() == "red"):
        GPIO.output(__PIN__RED,   True)
        GPIO.output(__PIN__GREEN, False)
        GPIO.output(__PIN__BLUE,  False)

    elif (my_color.lower() == "green"):
        GPIO.output(__PIN__RED,   False)
        GPIO.output(__PIN__GREEN, True)
        GPIO.output(__PIN__BLUE,  False)

    elif (my_color.lower() == "blue"):
        GPIO.output(__PIN__RED,   False)
        GPIO.output(__PIN__GREEN, False)
        GPIO.output(__PIN__BLUE,  True)

    elif (my_color.lower() == "purple"):
        GPIO.output(__PIN__RED,   True)
        GPIO.output(__PIN__GREEN, False)
        GPIO.output(__PIN__BLUE,  True)

    elif (my_color.lower() == "yellow"):
        GPIO.output(__PIN__RED,   True)
        GPIO.output(__PIN__GREEN, True)
        GPIO.output(__PIN__BLUE,  False)

    elif (my_color.lower() == "cyan"):
        GPIO.output(__PIN__RED,   False)
        GPIO.output(__PIN__GREEN, True)
        GPIO.output(__PIN__BLUE,  True)

    elif (my_color.lower() == "white"):
        GPIO.output(__PIN__RED,   True)
        GPIO.output(__PIN__GREEN, True)
        GPIO.output(__PIN__BLUE,  True)

    
def blink(time_interval=1000*__TIME_1MS):
    ## Clear outputs

    all_colors = ["black", "red", "green", "blue", "purple",
                  "yellow", "cyan", "white"]

    for my_color in all_colors:
        logger.info("Setting LED to %s" % my_color)
        set_led_color(my_color)
        time.sleep(time_interval)

def press_release_button(button,
                         high_delay=50*__TIME_1MS,
                         low_delay=10*__TIME_1MS):
    if (read_pin_value(button) == True):
        time.sleep(high_delay)
        if (read_pin_value(button) == True):
            while(read_pin_value(button) == True):
                time.sleep(low_delay)
            # Once the button is released, return True
            return True

        else:
            # The button was not pressed long enough, it might have been an
            # electrical bounce, so discard it and return False
            return False

def daemon_command(command, service):
    """
        0   success
        3   service not running
        5   couldn't stop service
        6   couldn't start service
    """
    result = subprocess.call(["sudo", "systemctl", command, service],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT
                             )
    return result

def set_color_by_status(service):
    result = daemon_command("status", service)
    if (result == 0):
        set_led_color("green")
    elif (result == 3):
        set_led_color("red")
    else:
        set_led_color("purple")
    return result

def monitor_buttons(time_interval=20*__TIME_1MS):
    time.sleep(time_interval)
    if (press_release_button(__PIN__BUTTON1)):
        result = set_color_by_status(my_service)
        if (result == 0):
            logger.info("Service [%s] is running already" % my_service)
        elif (result == 3):
            set_led_color("blue")
            logger.info("Service [%s] is not running... "
                  "Trying to start it" % my_service)

            result = daemon_command("start", my_service)
            set_color_by_status(my_service)

            if (result == 0):
                logger.info("Service [%s] started" % my_service)
            elif (result == 6):
                logger.info("Could not start Service [%s]" % my_service)

    if (press_release_button(__PIN__BUTTON2)):
        result = daemon_command("status", my_service)
        if (result == 3):
            logger.info("Service [%s] is stopped already" % my_service)
        elif (result == 0):
            set_led_color("blue")
            logger.info("Service [%s] is running... "
                  "Trying to stop it" % my_service)

            result = daemon_command("stop", my_service)
            set_color_by_status(my_service)

            if (result == 0):
                logger.info("Service [%s] stopped" % my_service)
            elif (result == 5):
                logger.info("Could not stop Service [%s]" % my_service)

################################################################################
## Main logic
if __name__ == '__main__':
    initialize()

    set_led_color("off")
    #my_service = "openvpn@js-lan-ca.service"
    my_service = "hostapd"

    result = set_color_by_status(my_service)
    if (result == 0):
        logger.info("Service [%s] is running" % my_service)
    elif (result == 3):
        logger.info("Service [%s] is not running" % my_service)

    while (True):
#        blink()
        monitor_buttons()

