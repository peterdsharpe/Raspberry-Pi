from sensors.temperature_mcp9808 import temperature
import time

thermometer_length = 80
thermometer_min_C = 21
thermometer_max_C = 27

print("Real-Time Temperature:")
while True:
    n_bars = (
        (temperature() - thermometer_min_C) /
        (thermometer_max_C - thermometer_min_C)
    ) * thermometer_length
    n_bars = int(round(n_bars))
    thermometer = n_bars * "#" + f' {temperature():.1f} deg C'

    print(thermometer)
    time.sleep(0.25)