# coding=utf-8
import cv2
from Perspective import Perspective
from Coordinates import Coordinates

if __name__ == "__main__":
    path = "book1.jpg"
    sourceImg = cv2.imread(path)


    persp = Perspective(sourceImg)
    persp.handle()  # 预处理
    edges = persp.edgesDetectCanny()  # Canny

    hull = persp.contourMethod(edges)  # 轮廓处理，获得符合要求的凸包
    hullCoord = Coordinates(hull)  # 检测凸包的坐标性质

    if hull is not None and hullCoord.quadCheck():  # 如果凸包不为空，且能近似构成四边形
        corners = hullCoord.calculateTRTLBRBL()
        correctedImg = persp.transform(corners)
        cv2.imshow("corrected Image", correctedImg)
        print "Yes. Correct the image successfully"
        cv2.waitKey(0)
    else:
        print "Laplacian"
        edges = persp.edgesDetectLaplacian()  # 拉普拉斯算子
        hull = persp.contourMethod(edges)
        hullCoord = Coordinates(hull)  # 检测凸包的坐标性质
        if hull is not None and hullCoord.quadCheck():  # 如果凸包不为空，且能近似构成四边形
            corners = hullCoord.calculateTRTLBRBL()
            correctedImg = persp.transform(corners)
            cv2.imshow("corrected Image", correctedImg)
            print "Yes. Correct the image successfully"
            cv2.waitKey(0)
        else:
            print "Sorry. Cannot correct the image"

    cv2.destroyAllWindows()
