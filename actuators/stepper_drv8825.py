import time
import RPi.GPIO as gpio
import numpy as np

gpio.setmode(gpio.BCM)


class Stepper_drv8825:
    def __init__(self,
                 dir_pin: int,
                 step_pin: int,
                 steps_per_revolution: float,
                 max_speed_steps_per_sec=100,
                 max_accel_steps_per_sec2=300,
                 move_smoothly=True,
                 ):
        # Initialize
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.steps_per_revolution = steps_per_revolution
        self.max_speed_steps_per_sec = max_speed_steps_per_sec
        self.max_accel_steps_per_sec2 = max_accel_steps_per_sec2
        self.move_smoothly = move_smoothly

        # Do some calculation
        self.degrees_per_step = 360 / self.steps_per_revolution

        # State variables
        self.current_position_steps: int = 0
        self.desired_position_steps: float = 0.
        self.dir_is_high: bool = False

        # Connect to RPi
        gpio.setup(self.dir_pin, gpio.OUT)
        gpio.setup(self.step_pin, gpio.OUT)

    def _set_dir_high(self):
        if not self.dir_is_high:
            gpio.output(self.dir_pin, gpio.HIGH)
            self.dir_is_high = True

    def _set_dir_low(self):
        if self.dir_is_high:
            gpio.output(self.dir_pin, gpio.LOW)
            self.dir_is_high = False

    def steps_to_degrees(self, steps):
        return steps * self.degrees_per_step

    def degrees_to_steps(self, degrees):
        return degrees / self.degrees_per_step

    def current_position_degrees(self):
        return self.steps_to_degrees(self.current_position_steps)

    def desired_position_degrees(self):
        return self.steps_to_degrees(self.desired_position_steps)

    def do_step(self, clockwise=True, delay=0.004):
        if clockwise:
            self._set_dir_high()
            self.current_position_steps += 1
        else:
            self._set_dir_low()
            self.current_position_steps -= 1

        gpio.output(self.step_pin, gpio.HIGH)
        time.sleep(delay / 2)
        gpio.output(self.step_pin, gpio.LOW)
        time.sleep(delay / 2)

    def move_steps(self, n_steps: int, _update_desired_position: bool = True):
        clockwise = n_steps > 0
        abs_n_steps = abs(n_steps)

        if _update_desired_position:
            self.desired_position_steps += n_steps

        if not self.move_smoothly:
            for i in range(abs_n_steps):
                self.do_step(
                    clockwise=clockwise,
                    delay=1 / self.max_speed_steps_per_sec
                )
        else:
            times_ramp = np.diff(  # Time between steps assoc. w/ constant angular acceleration
                np.sqrt(
                    2 * np.linspace(0, abs_n_steps, abs_n_steps + 1)
                    / self.max_accel_steps_per_sec2
                )
            )
            times = np.maximum.reduce([
                times_ramp,
                np.ones_like(times_ramp) / self.max_speed_steps_per_sec,
                times_ramp[::-1]
            ])
            for i in range(abs_n_steps):
                self.do_step(
                    clockwise=clockwise,
                    delay=times[i]
                )

    def goto_steps(self, step_target: int, _update_desired_position: bool = True):
        if _update_desired_position:
            self.desired_position_steps = step_target

        self.move_steps(
            n_steps=step_target - self.current_position_steps,
            _update_desired_position=False
        )

    def move_degrees(self, n_degrees: float):
        self.desired_position_steps += self.degrees_to_steps(n_degrees)

        self.goto_steps(
            step_target=round(self.desired_position_steps),
            _update_desired_position=False
        )

    def goto_degrees(self, degrees_target: float):
        self.desired_position_steps = self.degrees_to_steps(degrees_target)

        self.goto_steps(
            step_target=round(self.desired_position_steps),
            _update_desired_position=False
        )

    def reset_datum(self):
        self.current_position_steps = 0
        self.desired_position_steps = 0

    def cleanup(self):
        gpio.cleanup()
