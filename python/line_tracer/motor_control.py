
def motor_driver_init(pi, IN1, IN2):
    """
    モーター制御の初期化
    """
    # IN1, IN2をLOWに設定
    pi.write(IN1, 0)
    pi.write(IN2, 0)
    
    # IN1のPWM設定
    pi.set_PWM_frequency(IN1, 10000)
    pi.set_PWM_range(IN1, 100)
    pi.set_PWM_dutycycle(IN1, 0)
    
    # IN2のPWM設定
    pi.set_PWM_frequency(IN2, 10000)
    pi.set_PWM_range(IN2, 100)
    pi.set_PWM_dutycycle(IN2, 0)


def motor_pwm_init(pi, PWM):
    """
    モーターPWMの初期化
    """
    # PWMピンの設定
    pi.set_PWM_frequency(PWM, 10000)  # 周波数10kHz
    pi.set_PWM_range(PWM, 100)        # 範囲100
    pi.set_PWM_dutycycle(PWM, 0)      # デューティサイクル0%

def motor_control_update(pi, update_motor, MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2, MOTOR_PWM, MAX_VOLTAGE, BATTERY_VOLTAGE, LED_G, LED_R):
    """
    モーター制御を更新
    
    Args:
        pi: pigpioのインスタンス
        update_motor (bool): モーターを更新するかどうか
    """
    global motor_value, pwm_duty, motor_direction

    if not update_motor:
        # モーター制御をリセット
        motor_value = 0.0
        pwm_duty = 0
        pi.set_PWM_dutycycle(MOTOR_PWM, pwm_duty)
        pi.write(MOTOR1_IN1, 0)
        pi.write(MOTOR1_IN2, 0)
        pi.write(MOTOR2_IN1, 0)
        pi.write(MOTOR2_IN2, 0)
        pi.write(LED_G, 0)
        pi.write(LED_R, 0)
        motor_direction = 0
        return

    # モーター制御の更新処理
    motor_value = 0.0

    # モーター電圧の制限
    if motor_value > MAX_VOLTAGE:
        motor_value = MAX_VOLTAGE
    elif motor_value < -MAX_VOLTAGE:
        motor_value = -MAX_VOLTAGE

    # PWMデューティサイクルの計算
    pwm_duty = int(motor_value * 100.0 / BATTERY_VOLTAGE)

    # モーターの駆動方向に応じてGPIOピンを制御
    if pwm_duty >= 0:
        # 順転
        pi.set_PWM_dutycycle(MOTOR_PWM, 100)  # PWMを100%に設定

        pi.set_PWM_dutycycle(MOTOR1_IN1, pwm_duty)  # IN1にデューティサイクルを設定
        pi.set_PWM_dutycycle(MOTOR1_IN2, 0)         # IN2を0に設定
        pi.set_PWM_dutycycle(MOTOR2_IN1, pwm_duty)  # IN1にデューティサイクルを設定
        pi.set_PWM_dutycycle(MOTOR2_IN2, 0)         # IN2を0に設定

        pi.write(LED_G, 1)  # 緑LEDを点灯
        pi.write(LED_R, 0)  # 赤LEDを消灯
        motor_direction = 1
    else:
        # PWMデューティサイクルの絶対値を計算
        pwm_duty = abs(pwm_duty)
        # 逆転
        pi.set_PWM_dutycycle(MOTOR_PWM, 100)  # PWMを100%に設定

        pi.set_PWM_dutycycle(MOTOR1_IN1, 0)         # IN1を0に設定
        pi.set_PWM_dutycycle(MOTOR1_IN2, pwm_duty)  # IN2にデューティサイクルを設定
        pi.set_PWM_dutycycle(MOTOR2_IN1, 0)         # IN1を0に設定
        pi.set_PWM_dutycycle(MOTOR2_IN2, pwm_duty)  # IN2にデューティサイクルを設定

        pi.write(LED_G, 0)  # 緑LEDを消灯
        pi.write(LED_R, 1)  # 赤LEDを点灯
        motor_direction = 2