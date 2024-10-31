import pigpio
import time


MOTOR1_IN1 = 6
MOTOR1_IN2 = 5
MOTOR_PWM = 12

pi = pigpio.pi()

pi.set_mode(MOTOR_PWM, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN1, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN2, pigpio.OUTPUT)

pi.write(MOTOR1_IN1, 0)
pi.write(MOTOR1_IN2, 0)
pi.set_PWM_frequency(MOTOR1_IN1, 10000)
pi.set_PWM_range(MOTOR1_IN1, 100)
pi.set_PWM_dutycycle(MOTOR1_IN1, 0)
pi.set_PWM_frequency(MOTOR1_IN2, 10000)
pi.set_PWM_range(MOTOR1_IN2, 100)
pi.set_PWM_dutycycle(MOTOR1_IN2, 0)

time.sleep(1)
print("start motor control")

pi.set_PWM_dutycycle(MOTOR_PWM, 100)
pi.set_PWM_dutycycle(MOTOR1_IN1, 100)
pi.set_PWM_dutycycle(MOTOR1_IN2, 0)

pi.stop()


# gpio_pin0 = 18
# gpio_pin1 = 19

# pi = pigpio.pi()
# pi.set_mode(gpio_pin0, pigpio.OUTPUT)
# pi.set_mode(gpio_pin1, pigpio.OUTPUT)

# # GPIO18: 2Hz、duty比0.5
# pi.hardware_PWM(gpio_pin0, 2, 500000)
# # GPIO19: 8Hz、duty比0.1
# pi.hardware_PWM(gpio_pin1, 8, 100000)

# time.sleep(5)

# pi.set_mode(gpio_pin0, pigpio.INPUT)
# pi.set_mode(gpio_pin1, pigpio.INPUT)
# pi.stop()
