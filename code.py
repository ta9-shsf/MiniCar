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
    if Fdis >= 100 and RLdis <= 100 and RRdis <= 100:
      togikai_drive.Accel(FORWARD_S)
      togikai_drive.Steer(0)
      mode = "go"
    elif FLdis <= SHORT_DIST and FRdis >= SHORT_DIST:
        togikai_drive.Accel(FORWARD_C)
        togikai_drive.Steer(RIGHT)
        mode = "右旋回A"
    elif FLdis > SHORT_DIST and FRdis < SHORT_DIST:
        togikai_drive.Accel(FORWARD_C)
        togikai_drive.Steer(LEFT) 
        mode = "左旋回A"
    elif FLdis > SHORT_DIST and FRdis > SHORT_DIST:
        if (FLdis - FRdis) > 10:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(LEFT) 
            mode = "左旋回B"
        elif (FRdis - FLdis) > 10:
            togikai_drive.Accel(FORWARD_C)
            togikai_drive.Steer(RIGHT) 
            mode = "右旋回B"
        else:
            togikai_drive.Accel(FORWARD_S)
            togikai_drive.Steer(0)
            mode = "直進中B"
    else:
        togikai_drive.Accel(FORWARD_S)
        togikai_drive.Steer(0)
        mode = "直進中A"

    #表示
    print('時刻:{0:7.3f} 正面:{1:6.1f} , 右前:{2:6.1f} , 左前:{3:6.1f}, 右後:{4:6.1f} , 左後:{5:6.1f}, モード：{6}'.format( sim.getTime(),Fdis,FRdis,FLdis,RRdis,RLdis,mode))
