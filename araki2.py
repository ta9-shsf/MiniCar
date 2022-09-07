import os
import sys
sys.path.append('/home/pi/araki/togikai_function/')
import togikai_drive
import togikai_ultrasonic
import signal
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time
import numpy as np

# GPIOピン番号の指示方法
GPIO.setmode(GPIO.BOARD)

#超音波センサ初期設定
# Triger -- Fr:15, FrLH:13, RrLH:35, FrRH:32, RrRH:36
t_list=[15,13,35,32,36]
GPIO.setup(t_list,GPIO.OUT,initial=GPIO.LOW)
# Echo -- Fr:26, FrLH:24, RrLH:37, FrRH:31, RrRH:38
e_list=[26,24,37,31,38]
GPIO.setup(e_list,GPIO.IN)

#PWM制御の初期設定
##モータドライバ:PCA9685のPWMのアドレスを設定
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
##動作周波数を設定
pwm.set_pwm_freq(60)

#アライメント調整済みPWMパラメータ読み込み
PWM_PARAM = togikai_drive.ReadPWMPARAM(pwm)

#Gard 210523
#Steer Right
if PWM_PARAM[0][0] - PWM_PARAM[0][1] >= 100: #No change!
    PWM_PARAM[0][0] = PWM_PARAM[0][1] + 100  #No change!
    
#Steer Left
if PWM_PARAM[0][1] - PWM_PARAM[0][2] >= 100: #No change!
    PWM_PARAM[0][2] = PWM_PARAM[0][1] - 100  #No change!


#パラメータ設定
#右左折判定基準
Rshort = 60
Lshort = 60
#モーター出力
FORWARD_S = 100 #<=100
FORWARD_C = 70 #<=100
REVERSE = -60 #<=100
BRAKE = 0
#Stear
LEFT0 = 50
RIGHT0 = -50 #90
RIGHT1 = -100
LEFT3 = 90

RIGHT4 = -100
#SectionNumber
section = 0 #初期化
#BrakeTime
count = 0 #初期化

#データ記録用配列作成
d = np.zeros(6)
#操舵、駆動モーターの初期化
togikai_drive.Accel(PWM_PARAM,pwm,time,0)
togikai_drive.Steer(PWM_PARAM,pwm,time,0)

#一時停止（Enterを押すとプログラム実行開始）
print('Press any key to continue')
input()

#開始時間
start_time = time.time()


#ここから走行用プログラム
try:
    #変更したいグローバル変数がある場合は下記のように記述
    #global name_of_variable
    #global section
    #global count
    while True:
        #Frセンサ距離
        FRdis = togikai_ultrasonic.Mesure(GPIO,time,15,26)
        #FrLHセンサ距離
        LHdis = togikai_ultrasonic.Mesure(GPIO,time,13,24)
        #FrRHセンサ距離
        RHdis = togikai_ultrasonic.Mesure(GPIO,time,32,31)
        #RrLHセンサ距離
        RLHdis = togikai_ultrasonic.Mesure(GPIO,time,35,37)
        #RrRHセンサ距離
        RRHdis = togikai_ultrasonic.Mesure(GPIO,time,36,38)
        
        t = time.time() - start_time

        if section == 0:
            if t > 1.9:
                section = 1
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT1)
                mode = "section 1"
            elif (LHdis >= Lshort and LHdis < 200 )or RHdis <= 50:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT0)
                mode = "0,left"
            elif (RHdis >= Rshort and RHdis < 200 ) or LHdis <= 50:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT0)
                mode = "0,Right"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,0)
                mode = "0,else"
        ############
        # section1 #
        ############
        elif section == 1:
            if count > 15 and RRHdis < 70: 
                section = 2
                count = 0
                mode = "section 2"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT1)
                mode = "1,Right"
                count += 1
        ############
        # section2 #
        ############
        elif section == 2:
            if (FRdis <= 150 and count > 18) or count > 20:
                section = 3
                count = 0
                mode = "section 3"
            elif LHdis < 200 and LHdis >= Lshort:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT0)
                mode = "2,left"
                count += 1
            elif RHdis < 200 and RHdis >= Rshort:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT0)
                mode = "2,Right"
                count += 1
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT0)
                mode = "2,else"
                count += 1
                
        ############
        # section3 #
        ############
        elif section == 3:
            if (LHdis < 70 and count > 10) or count > 13:
                section = 4
                count = 0
                mode = "section 4"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT3)
                mode = "3,Left"
                count += 1
            
        ############
        # section4 #
        ############
        elif section == 4:
            if (RHdis < 70 and count > 10):
                section = 5
                count = 0
                mode = "section 5"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT4)
                mode = "4,Right"
                count += 1

        ############
        # section5 #
        ############               
        elif section == 5:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,0)
                mode = "5,Right"
                count += 1
            
            
        elif time.time()-start_time < 1:
            pass
        else:
            togikai_drive.Accel(PWM_PARAM,pwm,time,REVERSE)
            #togikai_drive.Accel(PWM_PARAM,pwm,time,0) #Stop if something is in front of you
            togikai_drive.Steer(PWM_PARAM,pwm,time,0)
            time.sleep(0.1)
            togikai_drive.Accel(PWM_PARAM,pwm,time,-100)
            togikai_drive.Steer(PWM_PARAM,pwm,time,0)
            GPIO.cleanup()
            #d = np.vstack([d,[time.time()-start_time, Fdis, FRdis, FLdis, RRdis, RLdis]])
            #np.savetxt('/home/pi/code/record_data.csv', d, fmt='%.3e')
            print('Stop!')
            break
        #距離データを配列に記録
        #d = np.vstack([d,[time.time()-start_time, FRdis, RHdis, LHdis, RRHdis, RLHdis]])
        #距離を表示
        print('Fr:{0:.1f} , FrRH:{1:.1f} , FrLH:{2:.1f}, RrRH:{3:.1f} , RrLH:{4:.1f} , mode:{5} , time:{6:.3f}'.format(FRdis,RHdis,LHdis,RRHdis,RLHdis,mode,time.time()-start_time))
        #time.sleep(0.01)

except KeyboardInterrupt:
    print('stop!')
    #np.savetxt('/home/pi/araki/record_data_araki.csv', d, fmt='%.3e')
    togikai_drive.Accel(PWM_PARAM,pwm,time,0)
    togikai_drive.Steer(PWM_PARAM,pwm,time,0)
    GPIO.cleanup()


