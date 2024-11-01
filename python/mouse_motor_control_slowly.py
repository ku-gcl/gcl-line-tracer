# ref: https://qiita.com/shi78ge/items/d4e8189094588b86a7b2

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

def ramp_motor(action, duration, start_speed=10, end_speed=100, step=10, delay=0.1):
    """
    モーターの速度を段階的に変更する関数
    :param action: 'forward' または 'backward'
    :param duration: 動作を維持する時間（秒）
    :param start_speed: 開始速度
    :param end_speed: 最大速度
    :param step: 速度の増加ステップ
    :param delay: ステップ間の遅延時間（秒）
    """
    speed = start_speed
    speed_increment = step if end_speed > start_speed else -step

    while (speed <= end_speed and speed_increment > 0) or (speed >= end_speed and speed_increment < 0):
        if action == 'forward':
            motor_value = speed
        elif action == 'backward':
            motor_value = -speed
        else:
            motor_value = 0.0

        update_motor = True if motor_value != 0.0 else False

        motor_control_update(pi, motor_value, update_motor, MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2,
                            MOTOR_PWM, MAX_VOLTAGE, BATTERY_VOLTAGE, LED_G, LED_R)
        print(f"{'前進' if motor_value > 0 else '後進'}: {speed} の速度で動作中")
        time.sleep(delay)
        speed += speed_increment

    # 最終速度に設定
    if action == 'forward':
        motor_value = end_speed
    elif action == 'backward':
        motor_value = -end_speed
    else:
        motor_value = 0.0

    update_motor = True if motor_value != 0.0 else False
    motor_control_update(pi, motor_value, update_motor, MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2,
                        MOTOR_PWM, MAX_VOLTAGE, BATTERY_VOLTAGE, LED_G, LED_R)

def move_forward(duration, start_speed=10, end_speed=100, step=10, delay=0.1):
    """指定した時間だけ前進し、速度を徐々に上げる"""
    ramp_motor('forward', duration, start_speed, end_speed, step, delay)
    print(f"前進を{duration}秒間維持")
    time.sleep(duration)
    stop_motor()

def move_backward(duration, start_speed=10, end_speed=100, step=10, delay=0.1):
    """指定した時間だけ後進し、速度を徐々に上げる"""
    ramp_motor('backward', duration, start_speed, end_speed, step, delay)
    print(f"後進を{duration}秒間維持")
    time.sleep(duration)
    stop_motor()

def stop_motor(duration=1):
    """モーターを停止する"""
    motor_control_update(pi, 0.0, False, MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2,
                        MOTOR_PWM, MAX_VOLTAGE, BATTERY_VOLTAGE, LED_G, LED_R)
    print(f"停止: {duration}秒")
    time.sleep(duration)

# メインループ
try:
    # 前進、停止、後進のシーケンス
    move_forward(duration=2, start_speed=10, end_speed=100, step=10, delay=0.2)    # 2秒間前進（速度10→100）
    move_backward(duration=4, start_speed=10, end_speed=100, step=10, delay=0.2)   # 4秒間後進（速度10→100）
    # 必要に応じて追加の動作をここに記述
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
