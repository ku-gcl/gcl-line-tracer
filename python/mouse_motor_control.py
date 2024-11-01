# ref: https://qiita.com/shi78ge/items/d4e8189094588b86a7b2

# import cv2
import time
import RPi.GPIO as GPIO
import pigpio
from line_tracer.motor_control import motor_driver_init, motor_pwm_init, motor_control_update

# モーターGPIOピンの設定
MOTOR1_IN1 = 6
MOTOR1_IN2 = 5
MOTOR2_IN1 = 19
MOTOR2_IN2 = 13
# LED GPIOピンの設定
LED_R = 17
LED_Y = 27
LED_G = 22

# モーターPWMピンの設定
MOTOR_PWM = 12

# バッテリー電圧と最大モーター電圧の設定
BATTERY_VOLTAGE = 2.6  # 実際のバッテリー電圧に変更
MAX_VOLTAGE = 3.0      # モーターに供給する最大電圧

# pigpioの初期化
pi = pigpio.pi()
if not pi.connected:
    exit()

# GPIOピンのモード設定
pi.set_mode(LED_R, pigpio.OUTPUT)
pi.set_mode(LED_Y, pigpio.OUTPUT)
pi.set_mode(LED_G, pigpio.OUTPUT)
pi.set_mode(MOTOR_PWM, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN1, pigpio.OUTPUT)
pi.set_mode(MOTOR1_IN2, pigpio.OUTPUT)
pi.set_mode(MOTOR2_IN1, pigpio.OUTPUT)
pi.set_mode(MOTOR2_IN2, pigpio.OUTPUT)

# LEDを消灯
pi.write(LED_R, 1)
pi.write(LED_Y, 1)
pi.write(LED_G, 1)
time.sleep(0.1)
pi.write(LED_Y, 1)

# モーターの初期化
motor_driver_init(pi, MOTOR1_IN1, MOTOR1_IN2)
motor_driver_init(pi, MOTOR2_IN1, MOTOR2_IN2)
motor_pwm_init(pi, MOTOR_PWM)

# 開始時刻を記録
start_time = time.time()
move_time1 = 2
stop_time = 1
move_time2 = 4

# メインループ
try:
    while True:
        # 経過時間を計算
        elapsed_time = time.time() - start_time

        if elapsed_time < move_time1:
            # 最初の3秒間はmotor_value=3.0
            motor_value = 3.0
            update_motor = True
        elif elapsed_time < move_time1 + stop_time:
            # 次の1秒間は停止
            motor_value = 0.0
            update_motor = False
        elif elapsed_time < move_time2 + stop_time:
            # その後3秒間はmotor_value=-3.0
            motor_value = -3.0
            update_motor = True
        else:
            # 全ての操作後はモーターを停止
            motor_value = 0.0
            update_motor = False

        # モーター制御の更新
        motor_control_update(pi, motor_value, update_motor, MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2,
                             MOTOR_PWM, MAX_VOLTAGE, BATTERY_VOLTAGE, LED_G, LED_R)
        time.sleep(0.1)  # 必要に応じてスリープ時間を調整

        if elapsed_time >= move_time2 + stop_time:
            break  # ループを終了

except KeyboardInterrupt:
    pass  # Ctrl+Cによる終了を許可

finally:
    # 終了時のクリーンアップ
    pi.write(LED_R, 0)
    pi.write(LED_Y, 0)
    pi.write(LED_G, 0)
    motor_control_update(pi, 0.0, False, MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2,
                         MOTOR_PWM, MAX_VOLTAGE, BATTERY_VOLTAGE, LED_G, LED_R)
    pi.stop()
