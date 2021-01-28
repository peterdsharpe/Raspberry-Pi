from actuators.stepper_drv8825 import Stepper_drv8825
import RPi.GPIO as gpio
import time

motor = Stepper_drv8825(
    dir_pin=27,
    step_pin=17,
    steps_per_revolution=200,
    max_speed_steps_per_sec=1500,
    max_accel_steps_per_sec2=2000,
    move_smoothly=True
)

while True:
    motor.goto_degrees(360)
    motor.goto_degrees(0)
