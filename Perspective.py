# coding=utf-8
# 图像变换类

import numpy as np
import cv2


class Perspective(object):
    def __init__(self, sourceImg):
        self.sourceImg = sourceImg
        self.greyImg = None
        self.shape = None
        self.destination = None


    def handle(self):
        # self.greyImg = cv2.GaussianBlur(self.sourceImg, (5, 5), 2)

        img = self.sourceImg
        self.shape = img.shape
        width = self.shape[1]
        height = self.shape[0]

        # TODO 将过大图像缩小或者过小图像放大
        if width > 400 or height > 300:
            self.sourceImg = cv2.pyrDown(self.sourceImg, (400, 400 * width / height))
        else:
            if width < 400 or height < 300:
                self.sourceImg = cv2.pyrUp(self.sourceImg, (400, 400 * width / height))

        # 显示原图
        cv2.namedWindow("image")
        cv2.imshow("image", self.sourceImg)
        cv2.waitKey(0)

        self.shape = self.sourceImg.shape
        width = self.shape[1]
        height = self.shape[0]

        self.destination = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

        self.greyImg = cv2.cvtColor(self.sourceImg, cv2.COLOR_BGR2GRAY)  # 图像灰度化
        print self.greyImg.shape[1]
        print self.greyImg.shape[0]

        # edges2 = cv2.Canny(img, 10, 100)  # 边缘检测
        # cv2.imshow("Canny",edges1)
        # cv2.imshow("Canny",edges2)
        # cv2.waitKey(0)
        # alpha = int(self.width * 0.5)
        # print alpha
        #
        # lines = cv2.HoughLines(edges, 1, np.pi / 180, alpha)
        # print "lines", len(lines[0])
        # lines1 = lines[0]
        # lines1.sort()
        #
        # for rho, theta in lines1:
        #     a = np.cos(theta)
        #     b = np.sin(theta)
        #     x0 = a * rho
        #     y0 = b * rho
        #     x1 = int(x0 + 200 * (-b))
        #     y1 = int(y0 + 200 * (a))
        #     x2 = int(x0 - 200 * (-b))
        #     y2 = int(y0 - 200 * (a))
        #     if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):
        #         cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        #     else:
        #         cv2.line(img, (x1, y1), (x2, y2), (255, 102, 21))
        #     cv2.imshow("lines", img)
        #     cv2.waitKey(0)

        # return edges1

    def edgesDetectCanny(self):
        return cv2.Canny(self.greyImg, 100, 150)

    def edgesDetectLaplacian(self):
        return cv2.Laplacian(self.greyImg, -1)

    def contourMethod(self, edges):
        hull = None
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓

        # for i, cnt in enumerate(contours):
        #     print "cv2.contourArea: ", i, " ", cv2.contourArea(cnt)
        #     cv2.imshow("contours of img", self.greyImg)
        #     cv2.drawContours(self.greyImg, contours, i, (0, 0, 0), 3)
        #     cv2.waitKey(0)

        # cntlist=[]
        # print self.area
        # print self.width
        # print self.height
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if hierarchy[0, i, 3] == -1 and area > 10000:
                    # print area/self.area
                    # print area
                    # cntlist.append()
                    hull = cv2.convexHull(cnt, returnPoints=True)
        return hull

    def transform(self, corners):
        corners = np.float32((corners[0][0], corners[1][0], corners[2][0], corners[3][0]))
        transformationMatrix = cv2.getPerspectiveTransform(corners, self.destination)
        warpedImage = cv2.warpPerspective(self.sourceImg, transformationMatrix, (self.shape[1], self.shape[0]))
        return warpedImage
