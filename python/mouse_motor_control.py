# ref: https://qiita.com/shi78ge/items/d4e8189094588b86a7b2

import cv2
import time
import RPi.GPIO as GPIO
import pigpio
from line_tracer.motor_control import motor_driver_init, motor_pwm_init, motor_control_update

# モーターGPIO
MOTOR1_IN1 = 6
MOTOR1_IN2 = 5
MOTOR2_IN1 = 19
MOTOR2_IN2 = 13
# LED GPIO
LED_R = 17
LED_Y = 27
LED_G = 22

# モーター回転速度制御GPIO(PWM)
MOTOR_PWM = 12

# バッテリー電圧
# TODO: 変更
BATTERY_VOLTAGE = 3.0

# モーターの正転/逆転制御GPIO
pi = pigpio.pi()
pi.set_mode(LED_R, pigpio.OUTPUT)
pi.set_mode(LED_Y, pigpio.OUTPUT)
pi.set_mode(LED_G, pigpio.OUTPUT)
pi.set_mode(MOTOR_PWM, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN1, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN2, pigpio.OUTPUT)
pi.set_mode(MOTOR2_IN1, pigpio.OUTPUT)
pi.set_mode(MOTOR2_IN2, pigpio.OUTPUT)

pi.write(LED_R, 1)
pi.write(LED_Y, 1)
pi.write(LED_G, 1)
motor_driver_init(pi, MOTOR1_IN1, MOTOR1_IN2)
motor_driver_init(pi, MOTOR2_IN1, MOTOR2_IN2)
motor_pwm_init(pi, MOTOR_PWM)



#モーター制御パラメータ
duty1 = 4  #直進時のDuty比
duty2 = 4  #旋回時のDuty比
freq = 700
sleep_time1 = 0.05  #直進時のモーター動作時間
sleep_time2 = 0.15  #旋回時のモーター動作時間

while True:
    motor_control_update()


