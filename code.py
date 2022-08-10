#パラメータ設定
#前壁との最小距離
Cshort = 30
#Cshort = 5
#右左折判定基準
RHshort0 = 250 #section0の右前判定
LHshort1 = 60 #section1の左前判定
RLHshort1 = 60 #section1の左後判定
Rshort = 100
Lshort = 60
short = 70
#モーター出力
FORWARD_S = 100 #<=100
FORWARD_C = 70 #<=100
REVERSE = -60 #<=100
BRAKE = 0
#Stear
LEFT0 = 50
RIGHT0 = -50 #90
RIGHT1 = -100
LEFT3 = 100
RIGHT4 = -100
LEFT5 = 100 #90
RIGHT5 = -100
LEFT6 = 100
RIGHT7 = -100
RIGHT8 = -100
LEFT8 = 100 #90
LEFT = 90 #<=100
RIGHT = -90 #<=100
#SectionNumber
section = 0 #初期化
#BrakeTime
count = 0 #初期化

def control_callback():
    #変更したいグローバル変数がある場合は下記のように記述
    #global name_of_variable
    
    global section
    global count

    
    #正面センサ距離取得
    FRdis = togikai_ultrasonic.Mesure(15,26)
    #左前センサ距離取得
    LHdis = togikai_ultrasonic.Mesure(13,24)
    #右前センサ距離取得
    RHdis = togikai_ultrasonic.Mesure(32,31)
    #左後センサ距離取得
    RLHdis = togikai_ultrasonic.Mesure(35,37)
    #右後センサ距離取得
    RRHdis = togikai_ultrasonic.Mesure(36,38)

    #加速、旋回の制御
    if section == 0:
        if RHdis >= RHshort0 and FRdis <= 180:
            section = 1
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(RIGHT1)
            mode = "section 1"
        elif LHdis >= Lshort:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(LEFT0)
            mode = "0,left"
        else:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(RIGHT0)
            mode = "0,Right"
    elif section == 1:
        if LHdis <= LHshort1 and RLHdis <= RLHshort1:
            section = 2
            count = 0
            mode = "section 2"
        else:
            if count <= 3:
                count += 1
                togikai_drive.Accel(BRAKE)
                togikai_drive.Steer(RIGHT1)
                mode = "1,RightBrake"
            else:
                togikai_drive.Accel(FORWARD_C)
                togikai_drive.Steer(RIGHT1)
                mode = "1,Right"
    elif section == 2:
        if LHdis - RLHdis > 100:
            section = 3
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(LEFT3)
            mode = "section3"     
        elif LHdis >= Lshort:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(LEFT)
            mode = "2,left"
        else:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(RIGHT)
            mode = "2,Right"
    elif section == 3:
        if FRdis >= 200 and RHdis >= 150:
            section = 4
            count = 0
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(RIGHT4)
            mode = "section4"     
        elif count <= 7:
            count += 1
            togikai_drive.Accel(count * 10)
            togikai_drive.Steer(LEFT3)
            mode = "3,LeftBrake"
        else:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(LEFT3)
            mode = "3,Left"
    elif section == 4:
        if RHdis >= 300:
            section = 5
            count = 0
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(RIGHT5)
            mode = "section5"
        elif count <= 3:
            count += 1
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(RIGHT4)
            mode = "4,RightBrake"
        else:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(RIGHT4)
            mode = "4,Right"
    elif section == 5:
        if LHdis >= 200 and FRdis <= 190:
            section = 6
            count = 0
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(LEFT6)
            mode = "section6"
        elif RHdis >= Rshort:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(RIGHT5)
            mode = "5,Right"
        else:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(LEFT5)
            mode = "5,Left"
    elif section == 6:
        if RHdis - RRHdis > 100:
            section = 7
            count = 0
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(RIGHT7)
            mode = "section7"
        elif count <= 3:
            count += 1
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(LEFT6)
            mode = "6,LeftBrake"
        else:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(LEFT6)
            mode = "6,Left"
    elif section == 7:
        if RHdis >= 300:
            section = 8
            count = 0
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(RIGHT8)
            mode = "section8"
        elif count <= 3:
            count += 1
            togikai_drive.Accel(BRAKE)
            togikai_drive.Steer(RIGHT7)
            mode = "7,RightBrake"
        else:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(RIGHT7)
            mode = "7,Right"
    elif section == 8:
        if FRdis >= 500:
            section = 0
            count = 0
            mode = "section0"
        elif RHdis >= Rshort:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(RIGHT8)
            mode = "8,Right"
        else:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(LEFT8)
            mode = "8,Left"
    
    else:
        togikai_drive.Accel(REVERSE)
        togikai_drive.Steer(0)
        mode = "Back"

    #距離を表示
    print('Time:{0:.3f} Fr:{1:.1f} , FrRH:{2:.1f} , FrLH:{3:.1f}, RrRH:{4:.1f} , RrLH:{5:.1f} , mode:{6}'.format(sim.getTime(),FRdis,RHdis,LHdis,RRHdis,RLHdis,mode))

