import os
import sys
sys.path.append('/home/pi/araki/togikai_function/')
import togikai_drive
import togikai_ultrasonic
import signal
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time
#import numpy as np

######################################
########## Initial Function ##########
######################################

##### GPIOピン番号の指示方法 #####
GPIO.setmode(GPIO.BOARD)

##### 超音波センサ初期設定 #####
# Triger -- Fr:15, FrLH:13, RrLH:35, FrRH:32, RrRH:36
t_list=[15,13,35,32,36]
GPIO.setup(t_list,GPIO.OUT,initial=GPIO.LOW)
# Echo -- Fr:26, FrLH:24, RrLH:37, FrRH:31, RrRH:38
e_list=[26,24,37,31,38]
GPIO.setup(e_list,GPIO.IN)

##### PWM制御の初期設定 #####
# モータドライバ:PCA9685のPWMのアドレスを設定
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
# 動作周波数を設定
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

#######################################
########## Parameter Setting ##########
#######################################

##### Section 0 #####
s0 = 50
l0 = 55
LEFT0 = 35
RIGHT0 = -35

##### Section 1 #####
RIGHT1 = -100

##### Accel Parameter #####
FORWARD_S = 100 #<=100
REVERSE = -60 #<=100
BRAKE = 0

##### Steer Parameter  #####
LEFT3 = 90
RIGHT4 = -100

##### Initialized #####
section = 0 #SectionNumber
count = 0 #ControlCycleCounter
time0 = 0
time1 = 0
time2 = 0
time3 = 0
time4 = 0
time5 = 0


##### データ記録用配列作成 #####
#d = np.zeros(6)

##### Accel & Steer parameter initialized #####
togikai_drive.Accel(PWM_PARAM,pwm,time,0)
togikai_drive.Steer(PWM_PARAM,pwm,time,0)

#################################################################
########## ----- Press Return Key to run program ----- ##########
#################################################################
print('Press Return key to continue')
input()

#開始時間
start_time = time.time()

#ここから走行用プログラム
try:
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

        #############
        # section 0 #
        #############
        if section == 0:
    
            time0 = t
            
            if t > 1.75:
                section = 1
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT1)
                mode = "section 1"
            elif RRHdis > RLHdis and RRHdis < 200 and RRHdis > l0 and RLHdis < s0:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT0)
                mode = "0,Right"
            elif RLHdis > RRHdis and RLHdis < 200 and RLHdis > l0 and RRHdis < s0:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT0)
                mode = "0,Left"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,0)
                mode = "0,else"

        #############
        # section 1 #
        #############
        elif section == 1:
            
            time1 = t - time0
            
            if time1 > 0.95:
                section = 2
                mode = "section 2"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT1)
                mode = "1,Right"
                count += 1

        #############
        # section 2 #
        #############
        elif section == 2:

            time2 = t - (time0 + time1)

            if time2 >= 0.7:
                section = 3
                mode = "section 3"
            elif RRHdis > RLHdis and RRHdis < 200 and RRHdis > l0 and RLHdis < s0:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT0)
                mode = "2,Right"
            elif RLHdis > RRHdis and RLHdis < 200 and RLHdis > l0 and RRHdis < s0:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT0)
                mode = "2,Left"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,0)
                mode = "2,else"
                
        #############
        # section 3 #
        #############
        elif section == 3:

            time3 = t - (time0 + time1 + time2)

            if time3 > 0.9:
                section = 4
                mode = "section 4"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT3)
                mode = "3,Left"
                count += 1
            
        #############
        # section 4 #
        #############
        elif section == 4:

            time4 = t - (time0 + time1 + time2 + time3)

            if time4 > 1.1:
                section = 5
                count = 0
                mode = "section 5"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT4)
                mode = "4,Right"
                count += 1

        #############
        # section 5 #
        #############               
        elif section == 5:

            time5 = t - (time0 + time1 + time2 + time3 + time4)

            togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
            togikai_drive.Steer(PWM_PARAM,pwm,time,-15)
            mode = "5,Right"
            count += 1    
        
        elif time.time()-start_time < 1:
            pass
        else:
            togikai_drive.Accel(PWM_PARAM,pwm,time,REVERSE)
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
    togikai_drive.Accel(PWM_PARAM,pwm,time,REVERSE)
    togikai_drive.Steer(PWM_PARAM,pwm,time,0)
    time.sleep(0.5)
    togikai_drive.Accel(PWM_PARAM,pwm,time,0)
    GPIO.cleanup()
