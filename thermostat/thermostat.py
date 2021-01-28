from actuators.stepper_drv8825 import Stepper_drv8825
from sensors.temperature_mcp9808 import temperature

motor = Stepper_drv8825(
    dir_pin=27,
    step_pin=17,
    steps_per_revolution=200,
    max_speed_steps_per_sec=1500,
    max_accel_steps_per_sec2=2000,
    move_smoothly=True
)

t_ref = temperature()

while True:
    motor.goto_degrees(
        (temperature() - t_ref) * 360
    )
