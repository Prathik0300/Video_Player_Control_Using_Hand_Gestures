import cv2 as cv
import numpy as np
import math

class Hand:
    def __init__(self,binary,masked,thresh,frame):
        self.contour=[]
        self.binary = binary
        self.masked=masked
        self.frame=frame
        self.thresh = thresh
        self.area=0
        self.outline = self.drawOutline()
        self.fingerTip = self.findFingertip()
    
    def drawOutline(self,min_area=10000):
        contour,_ = cv.findContours(self.binary,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        palmArea = 0
        flag=None
        cnt=None
        for (i,c) in enumerate(contour):
            area = cv.contourArea(c)
            if area>palmArea:
                palmArea=area
                self.area = area
                flag=i
        if flag is not None and palmArea>min_area:
            self.contour,cnt = contour[flag],contour[flag]
            copy = self.frame.copy()
            cv.drawContours(copy,[cnt],0,(0,255,0),2)
            return copy
        else:
            return self.frame

    def findFingertip(self):
        cnt = self.contour
        if len(cnt)==0:
            return cnt
        points = []
        hull = cv.convexHull(cnt,returnPoints=False)
        defects = cv.convexityDefects(cnt,hull)
        for i in range(defects.shape[0]):
            s,e,d,f = defects[i,0]
            end = tuple(cnt[e][0])
            points.append(end)
        filtered = self.filter_points(points,50)
        filtered.sort(key = lambda point:point[1] )
        return [pt for idx,pt in zip(range(5),filtered)]
    
    def filter_points(self,points,filter_val):
        for i in range(len(points)):
            for j in range(i+1,len(points)):
                if points[i] and  points[j] and self.dist(points[i],points[j])<filter_val:
                    points[j]=None
        filtered = []
        for i in points:
            if i is not None:
                filtered.append(i)
        return filtered
    
    def dist(self,p1,p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    
    def COM(self):
        if len(self.contour) == 0:
            return None
        M = cv.moments(self.contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return (cx,cy)
