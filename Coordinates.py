# coding=utf-8
import cv2

# 凸包的各坐标点计算类
class Coordinates(object):
    hull = None  # 凸包
    approx = None

    def __init__(self, hull):
        Coordinates.quad = 4
        Coordinates.corners = []
        self.hull = hull

    def quadCheck(self):  # 检查hull是否可以构成四边形
        peri = cv2.arcLength(self.hull, True) * 0.05  # 近似的误差大小
        self.approx = cv2.approxPolyDP(self.hull, peri, True)  # 近似凸包
        print "approx: ", self.approx

        if len(self.approx) == self.quad:
            print "is a quad"
            Coordinates.coord = self.approx.tolist()
            return True
        else:
            print "is not a quad"
            return False

    def calculateTRTLBRBL(self):
        print self.approx
        topoints = []
        bottompoints = []
        size = len(self.approx)
        sumY=0

        for i in range(0,size-1):
            sumY += self.approx[i][0][1]
        middleY = sumY/size
        for i, coord in enumerate(self.approx):
            coord = coord.tolist()
            if coord[0][1] < middleY:
                topoints.append(coord)
            else:
                bottompoints.append(coord)
        topLeft = min(topoints)
        topRight = max(topoints)
        bottomRight = max(bottompoints)
        bottomLeft = min(bottompoints)

        Coordinates.corners.append(topLeft)
        Coordinates.corners.append(topRight)
        Coordinates.corners.append(bottomRight)
        Coordinates.corners.append(bottomLeft)

        return Coordinates.corners