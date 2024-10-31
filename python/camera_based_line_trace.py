import cv2
import time
import RPi.GPIO as GPIO
import pigpio

#モーターの正転/逆転制御GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

#モーター回転速度制御GPIO(PWM)
gpio_pin0 = 12
gpio_pin1 = 13
pi = pigpio.pi()
pi.set_mode(gpio_pin0, pigpio.OUTPUT)

#モーター制御パラメータ
duty1 = 4  #直進時のDuty比
duty2 = 4  #旋回時のDuty比
freq = 700
sleep_time1 = 0.05  #直進時のモーター動作時間
sleep_time2 = 0.15  #旋回時のモーター動作時間

#カメラ設定
camera = cv2.VideoCapture(0)   
th = 50    # 二値化の閾値
i_max = 255

#カメラ画像のトリミングサイズ設定
trim_y = 180
trim_h = 30

#左ブロックエリア設定
LB_x1,LB_x2 = 200,210
LB_y1,LB_y2 = 0,trim_h

#右ブロックエリア設定
RB_x1,RB_x2 = 400,410
RB_y1,RB_y2 = 0,trim_h


while True:
    ret, frame = camera.read()    #フレームを取得
    frame = frame[trim_y:trim_y + trim_h,]  #画像をトリミング
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #グレースケール化
    ret, frame = cv2.threshold(frame, th, i_max, cv2.THRESH_BINARY_INV) #二値化（白黒反転）
    cv2.rectangle(frame,(LB_x1,LB_y1),(LB_x2,LB_y2),(0,0,255),1) #左ブロックエリア描画
    cv2.rectangle(frame,(RB_x1,RB_y1),(RB_x2,RB_y2),(0,0,255),1) #右ブロックエリア描画
    
    LB = frame[LB_y1:LB_y2,LB_x1:LB_x2] #左ブロックエリアのフレームをセット
    RB = frame[RB_y1:RB_y2,RB_x1:RB_x2] #右ブロックエリアのフレームをセット
 
    Det_LB = cv2.countNonZero(LB) #左ブロックエリアの白ピクセルカウント
    Det_RB = cv2.countNonZero(RB) #右ブロックエリアの白ピクセルカウント
    print("Det_LB: " +str(Det_LB) +" Det_RB: " +str(Det_RB))
 
    cv2.imshow('camera', frame)             # フレームを画面に表示
  
    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("エスケープが押されました")
        break

    #左右のブロックエリアへの接触を検出したら、停止線と判定して停止する
    elif Det_LB > 0 and Det_RB > 0:
        print("停止線への接触を検出しました")        
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        pi.hardware_PWM(gpio_pin0, freq, 000000)
        pi.hardware_PWM(gpio_pin1, freq, 000000)
        break
    
    #LB接触→右旋回
    elif Det_LB > 0:
        print("左ブロックエリアへの接触を検出しました")      
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
        pi.hardware_PWM(gpio_pin0, freq, duty2*100000)
        pi.hardware_PWM(gpio_pin1, freq, duty2*100000)
        time.sleep(sleep_time2)
        pi.hardware_PWM(gpio_pin0, freq, 000000)
        pi.hardware_PWM(gpio_pin1, freq, 000000)
        
    #RB接触→左旋回
    elif Det_RB > 0:
        print("右ブロックエリアへの接触を検出しました")
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
        pi.hardware_PWM(gpio_pin0, freq, duty2*100000)
        pi.hardware_PWM(gpio_pin1, freq, duty2*100000)
        time.sleep(sleep_time2)
        pi.hardware_PWM(gpio_pin0, freq, 000000)
        pi.hardware_PWM(gpio_pin1, freq, 000000)
        
    #ブロックエリアへの接触なし→前進
    else :
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        pi.hardware_PWM(gpio_pin0, freq, duty1*100000)
        pi.hardware_PWM(gpio_pin1, freq, duty1*100000)
        time.sleep(sleep_time1)
        pi.hardware_PWM(gpio_pin0, freq, 000000)
        pi.hardware_PWM(gpio_pin1, freq, 000000)
        
# 撮影用オブジェクトとウィンドウの解放
camera.release()
cv2.destroyAllWindows()

