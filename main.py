import cv2 as cv
import numpy as np
import gesture_recognition as gr
import vlc
import time
count=1


def filter(p1,p2):
    if abs(p1-p2)<50:
        return True
    return False

if __name__ == '__main__':
    video = cv.VideoCapture(0)
    hist = gr.capture_histogram()
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(r"C:\college\1st YEAR\RIVIERA 2K19\video_20190214_153435.mp4")
    player.set_media(media)
    player.play()
    countx=1
    county=1
    count =1
    while True:
        ret,frame = video.read()
        if not ret:
            break
        frame = cv.flip(frame,1)
        gr.detect_face(frame,block=True)
        hand = gr.detect_hand(frame,hist)
        temp = hand.drawOutline()
        outline = hand.drawOutline()
        quick_outline = hand.outline
        #area = Area(quick_outline)
        print(hand.area)
        fingertipList = hand.findFingertip()
        for fingertip in fingertipList:
            cv.circle(quick_outline,fingertip,5,(0,0,255),-1)
        com = hand.COM()
        if com:
            cv.circle(quick_outline,com,10,(255,0,0),-1)
        cv.imshow("HAND",quick_outline)
        if hand.area<30000:
            player.set_pause(1)
        else:
            player.set_pause(0)
        if com:
            #print("yes new com",county)
            #county+=1
            new_cx,new_cy = com[0],com[1]
            if count==1:
                old_cx,old_cy =new_cx,new_cy
                count+=1
            '''
            try:
                print("X",new_cx,old_cx)
                print("Y",new_cy,old_cy)
            except:
                pass
            '''
            if filter(new_cy,old_cy) and hand.area>30000:
                if new_cx<old_cx:
                    try:
                        player.set_time(player.get_time()-5000)
                        print("rewind",player.get_time())
                        time.sleep(1)
                    except:
                        print("except",player.get_time())

                else:
                    try:
                        player.set_time(player.get_time()+5000)
                        print("fast forward",player.get_time())
                        time.sleep(1)
                    except:
                        print("except",player.get_time())
            if filter(new_cx,old_cx) and hand.area>30000:
                if new_cy<old_cy:
                    try:
                        player.audio_set_volume(player.audio_get_volume() - 50)
                        print("vol down",player.audio_get_volume())
                        time.sleep(1)
                    except:
                        print("except",player.audio_get_volume())
                else:
                    try:
                        player.audio_set_volume(player.audio_get_volume() + 50)
                        print("vol up",player.audio_get_volume())
                        time.sleep(1)
                    except:
                        print("except",player.audio_get_volume())
            old_cx,old_cy = new_cx,new_cy
        else:
            pass
            #print("no new com",county)
            #county+=1
        if cv.waitKey(20) & 0xFF==ord('q'):
            break
    video.release()
    cv.destroyAllWindows()

