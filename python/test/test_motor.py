import pigpio
import time


MOTOR1_IN1 = 6
MOTOR1_IN2 = 5
MOTOR_PWM = 12

pi = pigpio.pi()

pi.set_mode(MOTOR_PWM, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN1, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN2, pigpio.OUTPUT)

# Motor 1
pi.write(MOTOR1_IN1, 0)
pi.write(MOTOR1_IN2, 0)

pi.set_PWM_frequency(MOTOR1_IN1, 10000)
pi.set_PWM_range(MOTOR1_IN1, 100)
pi.set_PWM_dutycycle(MOTOR1_IN1, 0)

pi.set_PWM_frequency(MOTOR1_IN2, 10000)
pi.set_PWM_range(MOTOR1_IN2, 100)
pi.set_PWM_dutycycle(MOTOR1_IN2, 0)

# PWM
pi.set_PWM_frequency(MOTOR_PWM, 10000)  # 周波数10kHz
pi.set_PWM_range(MOTOR_PWM, 100)        # 範囲100
pi.set_PWM_dutycycle(MOTOR_PWM, 0)

time.sleep(1)
start_time = time.time()

print("start motor control")
try:
    while (time.time()-start_time < 5):
        pwm_duty = 100
        
        pi.set_PWM_dutycycle(MOTOR_PWM, 100)  # PWMを100%に設定
        pi.set_PWM_dutycycle(MOTOR1_IN1, pwm_duty)  # IN1にデューティサイクルを設定
        pi.set_PWM_dutycycle(MOTOR1_IN2, 0)         # IN2を0に設定
        time.sleep(1)
finally:
    pi.set_PWM_dutycycle(MOTOR_PWM, 0)  # PWMを100%に設定
    pi.set_PWM_dutycycle(MOTOR1_IN1, 0)  # IN1にデューティサイクルを設定
    pi.set_PWM_dutycycle(MOTOR1_IN2, 0)         # IN2を0に設定


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
