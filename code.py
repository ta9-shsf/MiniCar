#パラメータ設定

#前壁との最小距離
Cshort=70

#右左折判定基準
SHORT_DIST = 90
CC_DIST = 150

#モーター出力
FORWARD_S = 100 #<=100
FORWARD_C = 50 #<=100
FORWARD_CC = 35
REVERSE = -60

#ステア
LEFT = 100 #<=100
RIGHT = -100 #<=100

def control_callback():
    #変更したいグローバル変数がある場合は下記のように記述
    #global name_of_variable
    
    #正面センサ距離取得
    Fdis = togikai_ultrasonic.Mesure(15,26)
    #左前センサ距離取得
    FLdis = togikai_ultrasonic.Mesure(13,24)
    #右前センサ距離取得
    FRdis = togikai_ultrasonic.Mesure(32,31)
    #左後センサ距離取得
    RLdis = togikai_ultrasonic.Mesure(35,37)
    #右後センサ距離取得
    RRdis = togikai_ultrasonic.Mesure(36,38)

    #加速、旋回の制御
    if RRdis > CC_DIST:
        togikai_drive.Accel(FORWARD_CC)
        togikai_drive.Steer(RIGHT)
        mode = "RIGHT_A"
    elif RLdis > CC_DIST:
        togikai_drive.Accel(FORWARD_CC)
        togikai_drive.Steer(LEFT)
        mode = "LEFT_A"
    elif FRdis > SHORT_DIST:
        togikai_drive.Accel(FORWARD_C)
        togikai_drive.Steer(RIGHT)
        mode = "RIGHT_B"
    elif FLdis > SHORT_DIST:
        togikai_drive.Accel(FORWARD_C)
        togikai_drive.Steer(LEFT)
        mode = "LEFT_B"
    else:
        togikai_drive.Accel(FORWARD_S)
        togikai_drive.Steer(0)
        mode = "直進中A"

    #表示
    print('時刻:{0:7.3f} 正面:{1:6.1f} , 右前:{2:6.1f} , 左前:{3:6.1f}, 右後:{4:6.1f} , 左後:{5:6.1f}, モード：{6}'.format( sim.getTime(),Fdis,FRdis,FLdis,RRdis,RLdis,mode))

